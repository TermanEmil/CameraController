from typing import Optional

from business.scheduling.timelapse_repository import TimelapseRepository
from enterprise.scheduling.timelapse import Timelapse


class CreateTimelapseBlRule:
    def __init__(self, timelapse_repository: TimelapseRepository):
        self._repository = timelapse_repository
        self._dto = None

    def set_params(self, dto: Timelapse):
        self._dto = dto
        return self

    def execute(self):
        self._repository.add(model=self._dto)


class RunTimelapseBlRul:
    def __init__(self):
        self._dto: Optional[Timelapse] = None

    def set_params(self, dto: Timelapse):
        self._dto = dto
        return self

    def execute(self):
        pass