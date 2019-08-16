from datetime import datetime


class CronScheduleViewModel:
    def __init__(
            self,
            pk: int,
            name: str,
            start_date: datetime,
            end_date: datetime,
            **kwargs):

        self.pk = pk
        self.name = name

        time_format = '{:%H:%M %d/%m}'
        self.start_date = time_format.format(start_date)
        self.end_date = time_format.format(end_date)