from typing import Iterable

from django.db import models


class CrudRepository:
    model: type(models.Model) = None
    dto_type: type = None

    def get_all(self) -> Iterable[dto_type]:
        instances = self.model.objects.all()

        for instance in instances:
            assert isinstance(instance, self.model)

            dto = self.dto_type(vars(instance))
            self._hard_map_objects(instance, dto)
            dto.pk = instance.pk
            yield dto

    def get(self, pk: int) -> dto_type:
        instance = self.model.objects.get(pk=pk)
        dto = self.dto_type()
        self._hard_map_objects(instance, dto)
        dto.pk = instance.pk
        return dto

    def add(self, model: dto_type):
        new_instance = self.model.objects.create(**vars(model))
        new_instance.save()

    def update(self, model: dto_type):
        db_model = self.model.objects.get(pk=model.pk)

        assert isinstance(db_model, self.model)
        for atr, value in model.__dict__.items():
            setattr(db_model, atr, value)

        db_model.save()

    def remove(self, pk: int):
        db_model = self.model.objects.get(pk=pk)
        assert isinstance(db_model, self.model)
        db_model.delete()

    @staticmethod
    def _hard_map_objects(obj1, obj2):
        for atr, value in obj1.__dict__.items():
            if atr in obj2.__dict__:
                setattr(obj2, atr, value)