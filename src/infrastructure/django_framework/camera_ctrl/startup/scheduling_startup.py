from adapters.scheduling.event_listeners import\
    CaptureErrorListener, CaptureTakenListener, \
    TimelapseEpisodeFinishedListener, TimelapseErrorListener
from adapters.scheduling.schedule_service import ScheduleService
from business.messaging.event_manager import EventManager
from business.timelapse.events import TimelapseEvents


class SchedulingStartup:
    def __init__(
            self,
            schedule_service: ScheduleService,
            event_manager: EventManager,
            capture_error_listener: CaptureErrorListener,
            capture_taken_listener: CaptureTakenListener,
            timelapse_episode_finished_listener: TimelapseEpisodeFinishedListener,
            timelapse_error_listener: TimelapseErrorListener):

        self._schedule_service = schedule_service
        self._event_manager = event_manager

        self._capture_error_listener = capture_error_listener
        self._capture_taken_listener = capture_taken_listener
        self._timelapse_episode_finished_listener = timelapse_episode_finished_listener
        self._timelapse_error_listener = timelapse_error_listener

    def run(self):
        self._init_scheduling()
        self._register_events()

    def _init_scheduling(self):
        self._schedule_service.run_startup_logic()

    def _register_events(self):
        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, self._capture_taken_listener.run)
        self._event_manager.register(TimelapseEvents.EPISODE_FINISHED, self._timelapse_episode_finished_listener.run)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, self._capture_error_listener.run)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, self._timelapse_error_listener.run)
