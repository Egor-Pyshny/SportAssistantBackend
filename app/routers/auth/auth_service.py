import os
import uuid
from datetime import datetime

from constants.prefixes import Prefixes
from constants.ttl import TTL
from dependencies import async_get_db, get_mail_sender_client, get_redis_client
from fastapi import HTTPException
from fastapi.params import Depends
from models import User
from passlib.handlers.sha2_crypt import sha256_crypt
from repositories.user.user_repository import UserRepository
from schemas.auth.email_validation_request import EmailValidationRequest
from schemas.auth.forgot_password_request import ForgotPasswordRequest
from schemas.auth.login_request import LoginRequest
from schemas.auth.redis_reset_password_data import RedisResetPasswordData
from schemas.auth.redis_session_data import RedisSessionData
from schemas.auth.registration_request import RegistrationRequest
from schemas.auth.resend_request import ResendRequest
from schemas.auth.reset_password_request import ResetPasswordRequest
from schemas.user.user_schema import UserSchema
from schemas.user.user_with_email_code import UserWithEmailCodeSchema
from services.mail import MailSender
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from utils.email_code_generator import generate_email_code
from utils.sid_generator import generate_sid


class AuthService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
        mail_client: MailSender = Depends(get_mail_sender_client),
    ):
        self.user_repository: UserRepository = UserRepository(db)
        self.redis_client: RedisClient = redis_client
        self.mail_client: MailSender = mail_client

    async def login(self, request: LoginRequest) -> str:
        user = await self.user_repository.get_user_by_email(request.email)
        password_hash = user.password.replace(
            "rounds=", f"rounds={int(os.getenv('HASH_ROUNDS', 535000))}"
        )
        if not user or not sha256_crypt.verify(request.password, password_hash):
            raise HTTPException(
                detail={"message": "Wrong email or password"},
                status_code=status.HTTP_403_FORBIDDEN,
            )
        session_id = generate_sid()
        redis_data = RedisSessionData(
            email=user.email,
            id=user.id,
        )
        self.redis_client.set(
            f"{Prefixes.redis_session_prefix.value}:{session_id}",
            redis_data.model_dump(mode="json"),
        )
        return session_id

    async def registration(self, request: RegistrationRequest):
        existing_user_redis = self.redis_client.exists(
            f"{Prefixes.redis_email_code_prefix.value}:{request.email}"
        )
        if existing_user_redis:
            redis_user = self.redis_client.get(f"{Prefixes.redis_email_code_prefix.value}:{request.email}")
            user = UserWithEmailCodeSchema.from_redis(redis_user)
            if user.device_id != request.device_id:
                raise HTTPException(
                    detail={"message": "Email at the verification stage"},
                    status_code=status.HTTP_409_CONFLICT,
                )
            else:
                self.redis_client.delete(f"{Prefixes.redis_email_code_prefix.value}:{request.email}")
        if await self.user_repository.is_unique_email(email=request.email):
            raise HTTPException(
                detail={"message": "Email already taken"},
                status_code=status.HTTP_409_CONFLICT,
            )
        rounds = int(os.getenv("HASH_ROUNDS", 535000))
        password_hash = sha256_crypt.hash(
            request.password,
            rounds=rounds,
        )
        password_hash = password_hash.replace(f"rounds={rounds}", "rounds=")
        user = UserSchema(
            id=uuid.uuid4(),
            **request.model_dump(exclude={"password"}),
            password=password_hash,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        code = generate_email_code()
        user_with_code = UserWithEmailCodeSchema(
            user=user,
            email_code=code,
            device_id=request.device_id
        )
        self.redis_client.set(
            f"{Prefixes.redis_email_code_prefix.value}:{user.email}",
            user_with_code.to_redis(),
            TTL.email_code_ttl.value,
        )
        # self.mail_client.send_email(request.email, "Verification code", code)
        # db_user = User(**user.model_dump())
        # await self.user_repository.create_user(db_user)
        # session_id = generate_sid()
        # redis_data = RedisSessionData(
        #     email=user.email,
        #     id=user.id,
        # )
        # self.redis_client.set(
        #     f"{Prefixes.redis_session_prefix.value}:{session_id}",
        #     redis_data.model_dump(mode="json"),
        # )
        # return session_id

    async def verify_email(self, request: EmailValidationRequest) -> str:
        user_json = self.redis_client.get(
            f"{Prefixes.redis_email_code_prefix.value}:{request.email}"
        )
        if not user_json:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Email is not in verification stage"},
            )
        user_with_code: UserWithEmailCodeSchema = UserWithEmailCodeSchema.from_redis(user_json)
        if user_with_code.email_code == request.code:
            user = User(**user_with_code.user.model_dump())
            await self.user_repository.create_user(user)
            self.redis_client.delete(f"{Prefixes.redis_email_code_prefix.value}:{request.email}")
            session_id = generate_sid()
            redis_data = RedisSessionData(
                email=user_with_code.user.email,
                id=user_with_code.user.id,
            )
            self.redis_client.set(
                f"{Prefixes.redis_session_prefix.value}:{session_id}",
                redis_data.model_dump(mode="json"),
            )
            return session_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Code is expired"}
            )

    async def logout(self, sid: str | None):
        if sid:
            if self.redis_client.exists(f"{Prefixes.redis_session_prefix.value}:{sid}"):
                self.redis_client.delete(f"{Prefixes.redis_session_prefix.value}:{sid}")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    async def resend_verification_code(self, request: ResendRequest):
        data = self.redis_client.get(f"{Prefixes.redis_email_code_prefix.value}:{request.email}")
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not in verification stage"},
            )
        new_code = generate_email_code()
        user_with_code: UserWithEmailCodeSchema = UserWithEmailCodeSchema.from_redis(data)
        user_with_code.email_code = new_code
        self.redis_client.set(
            f"{Prefixes.redis_email_code_prefix.value}:{request.email}",
            user_with_code.to_redis(),
            TTL.reset_password_code_ttl.value,
        )
        self.mail_client.send_email(request.email, "Verification code", new_code)

    async def forgot_password(self, request: ForgotPasswordRequest):
        user = await self.user_repository.get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"},
            )
        new_code = generate_email_code()
        self.redis_client.set(
            f"{Prefixes.redis_reset_password_code_prefix.value}:{user.email}",
            RedisResetPasswordData(code=new_code).model_dump(),
            TTL.reset_password_code_ttl.value,
        )
        self.mail_client.send_email(request.email, "Reset password", new_code)

    async def reset_password(self, request: ResetPasswordRequest):
        user = await self.user_repository.get_user_by_email(request.email)
        existing_user_redis = self.redis_client.exists(
            f"{Prefixes.redis_reset_password_code_prefix.value}:{request.email}"
        )
        if not user or not existing_user_redis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"},
            )
        code_json = self.redis_client.get(
            f"{Prefixes.redis_reset_password_code_prefix.value}:{request.email}"
        )

        if not code_json or not code_json["code"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"},
            )

        code = RedisResetPasswordData(code=code_json["code"])
        if code.code == request.code:
            rounds = int(os.getenv("HASH_ROUNDS", 535000))
            password_hash = sha256_crypt.hash(
                request.password,
                rounds=rounds,
            )
            new_password = password_hash.replace(f"rounds={rounds}", "rounds=")
            success = await self.user_repository.change_user_password(user.email, new_password)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"message": "Something went wrong..."},
                )
            self.redis_client.delete(
                f"{Prefixes.redis_reset_password_code_prefix.value}:{request.email}"
            )
        else:
            raise HTTPException(
                detail={"message": "Wrong code"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
