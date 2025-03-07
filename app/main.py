import uvicorn

from admin import CompetitionAdmin
from admin.coach_admin import CoachAdmin
from admin.user_admin import UserAdmin
from constants.prefixes import Prefixes
from constants.tags import Tags
from database import async_engine
from dependencies import authorized_only, get_redis_client
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.params import Depends
from routers.auth.auth_controller import auth_router
from routers.coach.coach_controller import coach_router
from routers.competition.competition_controller import competition_router
from routers.user.user_controller import user_router
from services.redis import RedisClient
from slowapi.errors import RateLimitExceeded
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI(debug=True)

admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(CoachAdmin)
admin.add_view(CompetitionAdmin)

origins = [
    # "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    concatenated_errors = "; ".join([error["msg"] for error in exc.errors()])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": {"message": concatenated_errors}}),
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": {"message": "Too many requests, please try again later."}},
    )


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(auth_router, prefix=Prefixes.auth.value, tags=Tags.auth.value)
app.include_router(user_router, prefix=Prefixes.user.value, tags=Tags.user.value)
app.include_router(coach_router, prefix=Prefixes.coach.value, tags=Tags.coach.value)
app.include_router(
    competition_router, prefix=Prefixes.competition.value, tags=Tags.competition.value
)


@app.get("/health_check", status_code=200)
def health_check():
    return "OK"


@app.get("/api/v1.0/test", status_code=200)
def test(
    request: Request,
    redis_client: RedisClient = Depends(get_redis_client),
    sid: str = Depends(authorized_only),
):
    if not sid or not redis_client.exists(f"{Prefixes.redis_session_prefix.value}:{sid}"):
        res = JSONResponse("Not authorized", status_code=status.HTTP_400_BAD_REQUEST)
        return res
    d = redis_client.get(sid)
    resp = JSONResponse(d)
    resp.set_cookie("sid", sid, httponly=True)
    return resp


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8000)
