import calendar
from datetime import date, timedelta
from typing import Optional

from constants.prefixes import Prefixes
from constants.strings import Strings
from dependencies import async_get_db, get_redis_client
from fastapi import Depends
from models import Competition, TrainingCamp
from repositories.competition.competition_repository import CompetitionRepository
from repositories.comprehensive_examination.comprehensive_examination_repository import (
    ComprehensiveExaminationRepository,
)
from repositories.med_examination.med_examination_repository import MedExaminationRepository
from repositories.notes.notes_repository import NotesRepository
from repositories.ofp_results.ofp_results_repository import OFPResultsRepository
from repositories.sfp_results.sfp_results_repository import SFPResultsRepository
from repositories.training_camp.training_camp_repository import TrainingCampRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.calendar.CalendarMonthData import CalendarMonthData, EventData, EventType
from schemas.note.note_schema import NoteSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession


class CalendarService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.competition_repository: CompetitionRepository = CompetitionRepository(db)
        self.camps_repository: TrainingCampRepository = TrainingCampRepository(db)
        self.notes_repository: NotesRepository = NotesRepository(db)
        self.ofp_repository: OFPResultsRepository = OFPResultsRepository(db)
        self.sfp_repository: SFPResultsRepository = SFPResultsRepository(db)
        self.med_repository: MedExaminationRepository = MedExaminationRepository(db)
        self.comprehensive_repository: ComprehensiveExaminationRepository = (
            ComprehensiveExaminationRepository(db)
        )
        self.redis_client: RedisClient = redis_client

    async def get_calendar_data(self, sid: str, month: int, year: int, day: Optional[int]):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        result = CalendarMonthData(eventDays={}, dayNotes={})
        last_day = calendar.monthrange(year, month)[1]
        start_month = date(day=1, month=month, year=year)
        end_month = date(day=last_day, month=month, year=year)
        competition_id = None
        camp_id = None
        if day:
            current_date = date(day=day, month=month, year=year)
            current_competitions = await self.competition_repository.get_all_current_competitions(
                user.id, current_date
            )
            current_camps = await self.camps_repository.get_all_current_camps(user.id, current_date)

            def sort_func(item: Competition | TrainingCamp):
                return item.start_date

            if len(current_competitions) > 0:
                current_competitions.sort(key=sort_func)
                result.competition = current_competitions[0]
                current_date = current_competitions[0].start_date
                competition_id = current_competitions[0].id
                while current_date <= current_competitions[0].end_date:
                    event = EventData(
                        name=f"{Strings.competitions_placeholder.value} {current_competitions[0].name}",
                        dates=[
                            current_competitions[0].start_date,
                            current_competitions[0].end_date,
                        ],
                        id=current_competitions[0].id,
                        type=EventType.COMPETITION,
                    )
                    if current_date in result.eventDays:
                        result.eventDays[current_date].append(event)
                    else:
                        result.eventDays[current_date] = [event]
                    current_date += timedelta(days=1)
            if len(current_camps) > 0:
                current_camps.sort(key=sort_func)
                result.camp = current_camps[0]
                current_date = current_camps[0].start_date
                camp_id = current_camps[0].id
                while current_date <= current_camps[0].end_date:
                    event = EventData(
                        name=f'{Strings.camp_placeholder.value} "{current_camps[0].location}"',
                        dates=[current_camps[0].start_date, current_camps[0].end_date],
                        id=current_camps[0].id,
                        type=EventType.CAMP,
                    )
                    if current_date in result.eventDays:
                        result.eventDays[current_date].append(event)
                    else:
                        result.eventDays[current_date] = [event]
                    current_date += timedelta(days=1)
        competitions = await self.competition_repository.get_competitions_between_dates(
            user.id, start_month, end_month
        )
        for competition in competitions:
            if competition.id == competition_id:
                continue
            current_date = competition.start_date
            while current_date <= competition.end_date and current_date <= end_month:
                event = EventData(
                    name=f"{Strings.competitions_placeholder.value} {competition.name}",
                    dates=[competition.start_date, competition.end_date],
                    id=competition.id,
                    type=EventType.COMPETITION,
                )
                if current_date in result.eventDays:
                    result.eventDays[current_date].append(event)
                else:
                    result.eventDays[current_date] = [event]
                current_date += timedelta(days=1)
        camps = await self.camps_repository.get_camps_between_dates(user.id, start_month, end_month)
        for camp in camps:
            if camp.id == camp_id:
                continue
            current_date = camp.start_date
            while current_date <= camp.end_date and current_date <= end_month:
                event = EventData(
                    name=f'{Strings.camp_placeholder.value} "{camp.location}"',
                    dates=[camp.start_date, camp.end_date],
                    id=camp.id,
                    type=EventType.CAMP,
                )
                if current_date in result.eventDays:
                    result.eventDays[current_date].append(event)
                else:
                    result.eventDays[current_date] = [event]
                current_date += timedelta(days=1)
        med_examinations = await self.med_repository.get_examinations_between_dates(
            user.id, start_month, end_month
        )
        for examination in med_examinations:
            event = EventData(
                name=f'{Strings.med_exam_placeholder.value} "{examination.institution}"',
                dates=[examination.date],
                id=examination.id,
                type=EventType.MED,
            )
            if examination.date in result.eventDays:
                result.eventDays[examination.date].append(event)
            else:
                result.eventDays[examination.date] = [event]
        comprehensive_examinations = (
            await self.comprehensive_repository.get_examinations_between_dates(
                user.id, start_month, end_month
            )
        )
        for examination in comprehensive_examinations:
            event = EventData(
                name=f'{Strings.comp_exam_placeholder.value} "{examination.institution}"',
                dates=[examination.date],
                id=examination.id,
                type=EventType.COMPREHENSIVE,
            )
            if examination.date in result.eventDays:
                result.eventDays[examination.date].append(event)
            else:
                result.eventDays[examination.date] = [event]
        ofp_results = await self.ofp_repository.get_examinations_between_dates(
            user.id, start_month, end_month
        )
        for ofp_result in ofp_results:
            event = EventData(
                name=f'{Strings.ofp_placeholder.value} "{ofp_result.ofp_category.name}"',
                dates=[ofp_result.date],
                id=ofp_result.id,
                type=EventType.OFP,
            )
            if ofp_result.date in result.eventDays:
                result.eventDays[ofp_result.date].append(event)
            else:
                result.eventDays[ofp_result.date] = [event]
        sfp_results = await self.sfp_repository.get_examinations_between_dates(
            user.id, start_month, end_month
        )
        for sfp_result in sfp_results:
            event = EventData(
                name=f'{Strings.sfp_placeholder.value} "{sfp_result.sfp_category.name}"',
                dates=[sfp_result.date],
                id=sfp_result.id,
                type=EventType.OFP,
            )
            if sfp_result.date in result.eventDays:
                result.eventDays[sfp_result.date].append(event)
            else:
                result.eventDays[sfp_result.date] = [event]
        notes = await self.notes_repository.get_notes_between_dates(user.id, start_month, end_month)
        for note in notes:
            result.dayNotes[note.date] = NoteSchema.model_validate(note)
        return result
