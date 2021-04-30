from typing import Optional

from enterprise.scheduling.scheduled_config import ScheduledConfig


class ScheduledConfigRepository:
    def get(self, pk: int) -> Optional[ScheduledConfig]:
        raise NotImplementedError()
