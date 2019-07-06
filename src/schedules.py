import json
from utils.time_utils import now


class Schedule:
    def __init__(self):
        self.name = self.__class__.__name__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, j):
        # This function will be used by the implementations.
        # It's a very generic way of loading an object from json.
        return cls(**j)

    # Abstract methods
    def time_until_next_img_capture(self):
        raise NotImplementedError()

    def get_next_capture_index(self):
        raise NotImplementedError()

    def has_ended(self):
        raise NotImplementedError()


class CounterSchedule(Schedule):
    def __init__(self, nb_of_captures, delta_time, start_time):
        super().__init__()

        self.nb_of_captures = nb_of_captures
        self.delta_time = delta_time
        self.start_time = start_time

    def time_until_next_img_capture(self):
        if self.has_ended():
            return None

        diff = now() - self.start_time
        return self.delta_time - diff % self.delta_time

    def get_next_capture_index(self):
        if self.has_ended():
            return None

        diff = now() - self.start_time
        result = diff / self.delta_time
        return int(result)

    def has_ended(self):
        return now() > self.start_time + self.delta_time * self.nb_of_captures


def deserialize_schedule(schedule_json):
    # If the schedule is a string, load it
    if type(schedule_json) == type(str):
        j = json.loads(schedule_json)
    else:
        j = schedule_json

    # Remove 'name' entry because nobody needs it anymore
    schedule_name = j['name']
    del j['name']

    if schedule_name == CounterSchedule.__name__:
        return CounterSchedule.from_json(j)
    else:
        return None
