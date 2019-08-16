from typing import Iterable


class FavouriteConfig:
    def __init__(self, pk: int, name: str):
        self.pk = pk
        self.name = name


class FavouriteConfigsRepository:
    def get_all(self) -> Iterable[FavouriteConfig]:
        raise NotImplementedError()

    def get(self, pk: int) -> FavouriteConfig:
        raise NotImplementedError()

    def add(self, favourite_config: FavouriteConfig):
        raise NotImplementedError()

    def update(self, favourite_config: FavouriteConfig):
        raise NotImplementedError()

    def remove(self, pk: int):
        raise NotImplementedError()