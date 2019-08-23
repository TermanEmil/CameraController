from adapters.scheduling.schedule_service import ScheduleService
from business.messaging.event_manager import EventManager
from business.timelapse.events import TimelapseEvents
from scheduling.events.all_photos_taken import all_photos_taken_log, all_photos_taken_log_to_db
from scheduling.events.capture_error import *
from scheduling.events.photo_taken import photo_taken_log, photo_taken_log_to_db


# noinspection PyMethodMayBeStatic
from scheduling.events.timelapse_error import timelapse_error_send_email, TimelapseErrorHardReset
from shared.di import obj_graph


class Startup:
    def __init__(
            self,
            camera_ctrl_service: CameraCtrlService,
            schedule_service: ScheduleService,
            event_manager: EventManager):

        self._camera_ctrl_service = camera_ctrl_service
        self._schedule_service = schedule_service
        self._event_manager = event_manager

    def run(self):
        self._check_autodetect_cameras_action()
        self._init_logging()
        self._init_scheduling()
        self._register_events()

    def _check_autodetect_cameras_action(self):
        settings = SettingsFacade()
        if settings.autodetect_cameras_on_start:
            try:
                self._camera_ctrl_service.cameras_autodetect()
            except Exception as e:
                logging.error('Failed to autodetect cameras on start. Error: {}'.format(e))

    def _init_logging(self):
        logging.getLogger('apscheduler').setLevel(logging.ERROR)

    def _init_scheduling(self):
        try:
            self._schedule_service.run_startup_logic()

        except Exception as e:
            logging.critical('Failed to run schedule_id startup. Error = {}'.format(e))

    def _register_events(self):
        self._event_manager.clear()

        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, photo_taken_log)
        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, photo_taken_log_to_db)

        self._event_manager.register(TimelapseEvents.ALL_PHOTOS_TAKEN, all_photos_taken_log)
        self._event_manager.register(TimelapseEvents.ALL_PHOTOS_TAKEN, all_photos_taken_log_to_db)

        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_log)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_send_email)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_log_to_db)

        timelapse_error_hard_reset = obj_graph().provide(TimelapseErrorHardReset)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, timelapse_error_hard_reset.run)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, timelapse_error_send_email)