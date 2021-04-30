from typing import Optional

from business.scheduling import scheduled_config_repository
from camera_ctrl.models import scheduling_models as models
from enterprise.scheduling.scheduled_config import ScheduledConfig, Config


class ScheduledConfigRepository(scheduled_config_repository.ScheduledConfigRepository):
    def get(self, pk: int) -> Optional[ScheduledConfig]:
        scheduled_configs = models.ScheduledConfig.objects.filter(pk=pk)
        if len(scheduled_configs) == 0:
            return None

        scheduled_config = scheduled_configs[0]
        configs = [Config(name=field.name, value=field.value) for field in scheduled_config.fields.all()]
        return ScheduledConfig(name=scheduled_config.name, configs=configs)