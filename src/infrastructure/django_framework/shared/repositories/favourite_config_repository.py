from typing import Iterable, Optional

from adapters.camera.configs import favourite_configs_repository
from adapters.camera.configs.favourite_configs_repository import FavouriteConfig
from camera_ctrl.models.camera_config_models import FavField


class FavouriteConfigRepository(favourite_configs_repository.FavouriteConfigsRepository):
    def get_all(self) -> Iterable[favourite_configs_repository.FavouriteConfig]:
        fav_fields = FavField.objects.all()

        for field in fav_fields:
            assert isinstance(field, FavField)
            yield favourite_configs_repository.FavouriteConfig(pk=field.pk, name=field.name)

    def get(self, pk: int) -> Optional[FavouriteConfig]:
        fav_config = FavField.objects.get(pk=pk)

        assert isinstance(fav_config, FavField)
        return FavouriteConfig(pk=fav_config.pk, name=fav_config.name)

    def add(self, favourite_config: FavouriteConfig):
        new_field = FavField.objects.create(name=favourite_config.name)
        new_field.save()

    def update(self, favourite_config: FavouriteConfig):
        db_fav_field = FavField.objects.get(pk=favourite_config.pk)

        assert isinstance(db_fav_field, FavField)
        db_fav_field.name = favourite_config.name
        db_fav_field.save()

    def remove(self, pk: int):
        db_fav_field = FavField.objects.get(pk=pk)
        assert isinstance(db_fav_field, FavField)
        db_fav_field.delete()


