from typing import Annotated, Optional

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Depends, Query, Response
from routers.calendar.calendar_service import CalendarService
from schemas.calendar.CalendarMonthData import CalendarMonthData

calendar_router = APIRouter()


@calendar_router.get(path=Urls.calendar_get.value, response_model=CalendarMonthData)
async def get_calendar_data(
    response: Response,
    month: Annotated[int, Query()],
    year: Annotated[int, Query()],
    day: Annotated[Optional[int], Query()] = None,
    sid: str | None = Depends(authorized_only),
    calendar_service: CalendarService = Depends(CalendarService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await calendar_service.get_calendar_data(sid, month, year, day)
