import logging

from adapters.app_logging.persistent_logger import PersistentLogger
from adapters.scheduling.notifications_settings import NotificationsSettings
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogType
from enterprise.camera_ctrl.camera import Camera
from enterprise.scheduling.scheduled_config import Config


class ConfigSetListener(PersistentLogger):
    log_type = LogType.INFO
    category = 'ScheduledConfig'
    title = 'Config set'

    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            log_manager: LogManager):

        super().__init__(log_manager)
        self._settings = notifications_settings
        self._log_manager = log_manager

    def run(self, config_field: Config, camera: Camera, initial_config_value: str, **kwargs):
        msg = f'Changed {config_field.name} from {initial_config_value} to {config_field.value} on {camera.name}'
        logging.info(msg)
        self.persistent_log(msg)

