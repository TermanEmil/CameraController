from typing import Callable, Dict


class EventManager:
    def __init__(self):
        self._events_dict: Dict[str, list] = dict()

    def clear(self):
        self._events_dict.clear()

    def register(self, event_name: str, func: Callable):
        if event_name not in self._events_dict:
            self._events_dict[event_name] = []

        self._events_dict[event_name].append(func)

    def trigger_event(self, event_name: str, kwargs):
        if event_name not in self._events_dict:
            return

        for event_f in self._events_dict[event_name]:
            event_f(**kwargs)
