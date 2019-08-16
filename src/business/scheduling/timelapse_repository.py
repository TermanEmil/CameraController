from typing import Iterable

from enterprise.scheduling.timelapse import Timelapse


class TimelapseRepository:
    def get_all(self) -> Iterable[Timelapse]:
        raise NotImplementedError()

    def get(self, pk: int) -> Timelapse:
        raise NotImplementedError()

    def add(self, model: Timelapse):
        raise NotImplementedError()

    def update(self, model: Timelapse):
        raise NotImplementedError()

    def remove(self, pk: int):
        raise NotImplementedError()