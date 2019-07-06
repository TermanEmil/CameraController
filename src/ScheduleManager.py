import os
import json
import schedules


class ScheduleManager:
    c_default_schedule_file_path = './current_schedule.json'

    def __init__(self, schedule_file_path=None):
        if schedule_file_path is None:
            self.schedule_file_path = ScheduleManager.c_default_schedule_file_path
        else:
            self.schedule_file_path = schedule_file_path

        self.current_schedule = None

    def pick_schedule(self, default_schedule=None):
        # If there already exists a valid schedule, choose that one.
        existing_schedule = self._find_existing_schedule()

        if existing_schedule is None or existing_schedule.has_ended():
            return default_schedule

        return existing_schedule

    def start_schedule(self, schedule):
        assert isinstance(schedule, schedules.Schedule)
        self.current_schedule = schedule

        self._save_schedule()

    def _find_existing_schedule(self):
        if not os.path.exists(self.schedule_file_path):
            return None

        with open(self.schedule_file_path) as f:
            j = json.load(f)

        return schedules.deserialize_schedule(j)

    def _save_schedule(self):
        assert isinstance(self.current_schedule, schedules.Schedule)

        with open(ScheduleManager.c_default_schedule_file_path, 'w') as f:
            f.write(self.current_schedule.to_json())
