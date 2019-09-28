from typing import Iterable

from .favourite_configs_repository import FavouriteConfigsRepository, FavouriteConfig


class FavouriteConfigsService:
    def __init__(self, favourite_config_repository: FavouriteConfigsRepository):
        self._favourite_config_repository = favourite_config_repository

    def get_all(self) -> Iterable[FavouriteConfig]:
        return self._favourite_config_repository.get_all()

    def add(self, config_name: str):
        fav_config = FavouriteConfig(pk=-1, name=config_name)
        self._favourite_config_repository.add(favourite_config=fav_config)

    def update(self, pk: int, config_name: str):
        fav_config = FavouriteConfig(pk=pk, name=config_name)
        self._favourite_config_repository.update(fav_config)

    def remove(self, pk: int):
        self._favourite_config_repository.remove(pk=pk)

