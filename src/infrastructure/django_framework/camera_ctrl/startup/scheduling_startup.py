from adapters.scheduling.event_listeners import\
    CaptureErrorListener, CaptureTakenListener, \
    TimelapseEpisodeFinishedListener, TimelapseErrorListener
from adapters.scheduling.event_listeners.config_failed_change_listener import ConfigFailedChangeListener
from adapters.scheduling.event_listeners.config_failed_get_listener import ConfigFailedGetListener
from adapters.scheduling.event_listeners.config_failed_set_listener import ConfigFailedSetListener
from adapters.scheduling.event_listeners.config_missing_listener import ConfigMissingListener
from adapters.scheduling.event_listeners.config_set_listener import ConfigSetListener
from adapters.scheduling.schedule_service import ScheduleService
from business.messaging.event_manager import EventManager
from business.scheduled_configs.events import ScheduledConfigEvents
from business.timelapse.events import TimelapseEvents


class TimelapseSchedulingStartup:
    def __init__(
            self,
            event_manager: EventManager,
            capture_error_listener: CaptureErrorListener,
            capture_taken_listener: CaptureTakenListener,
            timelapse_episode_finished_listener: TimelapseEpisodeFinishedListener,
            timelapse_error_listener: TimelapseErrorListener):

        self._event_manager = event_manager

        self._capture_error_listener = capture_error_listener
        self._capture_taken_listener = capture_taken_listener
        self._timelapse_episode_finished_listener = timelapse_episode_finished_listener
        self._timelapse_error_listener = timelapse_error_listener

    def register_events(self):
        self._event_manager.register(TimelapseEvents.PHOTO_TAKEN, self._capture_taken_listener.run)
        self._event_manager.register(TimelapseEvents.EPISODE_FINISHED, self._timelapse_episode_finished_listener.run)
        self._event_manager.register(TimelapseEvents.CAPTURE_ERROR, self._capture_error_listener.run)
        self._event_manager.register(TimelapseEvents.TIMELAPSE_ERROR, self._timelapse_error_listener.run)


class ScheduledConfigSchedulingStartup:
    def __init__(
            self,
            event_manager: EventManager,
            config_set_listener: ConfigSetListener,
            config_failed_get_listener: ConfigFailedGetListener,
            config_missing_listener: ConfigMissingListener,
            config_failed_set_listener: ConfigFailedSetListener,
            config_failed_change_listener: ConfigFailedChangeListener):

        self._event_manager = event_manager

        self._config_missing_listener = config_missing_listener
        self._config_failed_get_listener = config_failed_get_listener
        self._config_failed_set_listener = config_failed_set_listener
        self._config_failed_change_listener = config_failed_change_listener
        self._config_set_listener = config_set_listener

    def register_events(self):
        self._event_manager.register(ScheduledConfigEvents.CONFIG_SET, self._config_set_listener.run)
        self._event_manager.register(ScheduledConfigEvents.CONFIG_GET_ERROR, self._config_failed_get_listener.run)
        self._event_manager.register(ScheduledConfigEvents.CONFIG_MISSING, self._config_missing_listener.run)
        self._event_manager.register(ScheduledConfigEvents.CONFIG_SET_ERROR, self._config_failed_set_listener.run)
        self._event_manager.register(ScheduledConfigEvents.CONFIG_FAILED_TO_CHANGE_ERROR, self._config_failed_change_listener.run)


class SchedulingStartup:
    def __init__(
            self,
            schedule_service: ScheduleService,
            timelapse_scheduling_startup: TimelapseSchedulingStartup,
            scheduled_config_scheduling_startup: ScheduledConfigSchedulingStartup):

        self._schedule_service = schedule_service
        self._timelapse_scheduling_startup = timelapse_scheduling_startup
        self._scheduled_config_scheduling_startup = scheduled_config_scheduling_startup

    def run(self):
        self._init_scheduling()
        self._register_events()

    def _init_scheduling(self):
        self._schedule_service.run_startup_logic()

    def _register_events(self):
        self._timelapse_scheduling_startup.register_events()
        self._scheduled_config_scheduling_startup.register_events()
