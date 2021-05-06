import logging

from adapters.app_logging.persistent_logger import PersistentLogger
from adapters.emailing.email_service import EmailService
from adapters.scheduling.notifications_settings import NotificationsSettings
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogType
from enterprise.camera_ctrl.camera import Camera
from enterprise.scheduling.scheduled_config import Config


class ConfigFailedSetListener(PersistentLogger):
    log_type = LogType.ERROR
    category = 'ScheduledConfig'
    title = 'Failed to set config'

    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            log_manager: LogManager,
            email_service: EmailService):

        super().__init__(log_manager)
        self._settings = notifications_settings
        self._email_service = email_service

    def run(self, config_field: Config, camera: Camera, exception: Exception, **kwargs):
        msg = f'Failed to set {config_field.name} to {config_field.value} on {camera.name}: {exception}'

        logging.error(msg)

        self.persistent_log(msg)
        self._email_service.send_email(subject=self.title, message=msg)

