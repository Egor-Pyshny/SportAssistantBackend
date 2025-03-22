import uvicorn
from admin import CompetitionAdmin
from admin.coach_admin import CoachAdmin
from admin.ofp_category_admin import OFPCategoryAdmin
from admin.sfp_category_admin import SFPCategoryAdmin
from admin.user_admin import UserAdmin
from constants.prefixes import Prefixes
from constants.tags import Tags
from database import async_engine
from dependencies import authorized_only, get_redis_client
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.params import Depends
from routers.ant_params.ant_params_controller import ant_params_router
from routers.auth.auth_controller import auth_router
from routers.coach.coach_controller import coach_router
from routers.competition.competition_controller import competition_router
from routers.comprehensive_examination.comprehensive_examination_controller import (
    comprehensive_exams_router,
)
from routers.med_examination.med_examination_controller import med_exams_router
from routers.note.note_controller import notes_router
from routers.ofp_results.ofp_results_controller import ofp_results_router
from routers.sfp_results.sfp_results_controller import sfp_results_router
from routers.training_camp.training_camp_controller import training_camp_router
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
admin.add_view(OFPCategoryAdmin)
admin.add_view(SFPCategoryAdmin)

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


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": {"message": "Too many requests, please try again later."}},
    )


app.include_router(auth_router, prefix=Prefixes.auth.value, tags=Tags.auth.value)
app.include_router(user_router, prefix=Prefixes.user.value, tags=Tags.user.value)
app.include_router(coach_router, prefix=Prefixes.coach.value, tags=Tags.coach.value)
app.include_router(
    competition_router, prefix=Prefixes.competition.value, tags=Tags.competition.value
)
app.include_router(training_camp_router, prefix=Prefixes.camps.value, tags=Tags.camps.value)
app.include_router(ofp_results_router, prefix=Prefixes.ofp_results.value, tags=Tags.ofp.value)
app.include_router(sfp_results_router, prefix=Prefixes.sfp_results.value, tags=Tags.sfp.value)
app.include_router(ant_params_router, prefix=Prefixes.ant_params.value, tags=Tags.ant_params.value)
app.include_router(notes_router, prefix=Prefixes.notes.value, tags=Tags.notes.value)
app.include_router(
    comprehensive_exams_router,
    prefix=Prefixes.comprehensive_examination.value,
    tags=Tags.comprehensive_examination.value,
)
app.include_router(
    med_exams_router, prefix=Prefixes.med_examination.value, tags=Tags.med_examination.value
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
