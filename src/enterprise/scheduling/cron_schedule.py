from datetime import datetime, timedelta

import pytz
from dateutil.tz import tz


class CronSchedule:
    def __init__(
            self,
            pk: int = None,
            name: str = 'CronSchedule',

            start_date: datetime = None,
            end_date: datetime = None,

            year: str = '*',
            month: str = '*',
            day: str = '*',
            week: str = '*',
            day_of_week: str = '*',
            hour: str = '*',
            minute: str = '*',
            second: str = '*',
            **kwargs):

        if start_date is None:
            start_date = self.default_start_date()

        if end_date is None:
            end_date = self.default_end_date(start_date)

        self.pk = pk
        self.name = name

        self.start_date = start_date
        self.end_date = end_date

        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def default_start_date():
        return datetime.now(tz=pytz.utc)

    @staticmethod
    def default_end_date(start):
        return start + timedelta(days=1)



