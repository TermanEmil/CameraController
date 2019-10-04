from adapters.scheduling.schedule_service import ScheduleService
from business.messaging.event_manager import EventManager
from business.timelapse.events import TimelapseEvents
from camera_ctrl.events.scheduling.all_photos_taken import *
from camera_ctrl.events.scheduling.capture_error import *
from camera_ctrl.events.scheduling.photo_taken import photo_taken_log, photo_taken_log_to_db
from camera_ctrl.events.scheduling.timelapse_error import TimelapseErrorHardReset, TimelapseErrorSendEmail
from shared.di import obj_graph


class SchedulingStartup:
    def __init__(
            self,
            schedule_service: ScheduleService,
            event_manager: EventManager):

        self._schedule_service = schedule_service
        self._event_manager = event_manager

    def run(self):
        self._init_scheduling()
        self._register_events()

    def _init_scheduling(self):
        try:
            self._schedule_service.run_startup_logic()

        except Exception as e:
            logging.critical('Failed to run schedule_id startup. Error = {}'.format(e))

    def _register_events(self):
        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, photo_taken_log)
        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, photo_taken_log_to_db)

        self._event_manager.register(TimelapseEvents.ALL_PHOTOS_TAKEN, all_photos_taken_log)
        self._event_manager.register(TimelapseEvents.ALL_PHOTOS_TAKEN, all_photos_taken_log_to_db)

        capture_error_send_email: CaptureErrorSendEmail = obj_graph().provide(CaptureErrorSendEmail)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_log)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_send_email.run)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, capture_error_log_to_db)

        timelapse_error_hard_reset = obj_graph().provide(TimelapseErrorHardReset)
        timelapse_error_send_email = obj_graph().provide(TimelapseErrorSendEmail)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, timelapse_error_hard_reset.run)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, timelapse_error_send_email.run)