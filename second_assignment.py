from datetime import datetime, time
import json

# Single Responsibility Principle:
# The Event class only manages event-specific details.
# FileHandler class is only responsible for file operations.
# EventScheduler is responsible for scheduling logic


class Event:
    def __init__(self, start_time, end_time):
        self.start_time = datetime.fromisoformat(start_time)
        self.end_time = datetime.fromisoformat(end_time)


class FileHandler:
    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_to_file(data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)


class EventScheduler:
    def __init__(self):
        self.events = []
        self.last_end_time = None
        self.available_slots_by_date = {}

    # Open-Closed Principle: 
    # Logic for loading events can be extended without modifying this class.
    def load_events(self, file_path):
        events_data = FileHandler.load_from_file(file_path)
        self.events = [Event(event['start']['dateTime'],
                             event['end']['dateTime']) for event in events_data]

    def sort_events(self):
        self.events.sort(key=lambda event: event.start_time)
        if self.events:
            earliest_date = self.events[0].start_time.date()
            tz_info = self.events[0].start_time.tzinfo
            self.last_end_time = datetime.combine(
                earliest_date, time(0, 0), tz_info)

    def calculate_available_slots(self):
        midnight = time(0, 0)
        end_of_day = time(23, 59, 59)

        for event in self.events:
            current_date = self.last_end_time.date().isoformat()

            # If a new day begins, add a slot from 00:00:00 to the first event for that day.
            if event.start_time.date() != self.last_end_time.date():
                self.available_slots_by_date[current_date].append({
                    'start_time': self.last_end_time.time().isoformat(),
                    'end_time': end_of_day.isoformat()
                })

                current_date = event.start_time.date().isoformat()
                self.last_end_time = datetime.combine(
                    event.start_time.date(), midnight, self.last_end_time.tzinfo)

                self.available_slots_by_date[current_date] = []
                self.available_slots_by_date[current_date].append({
                    'start_time': midnight.isoformat(),
                    'end_time': event.start_time.time().isoformat()
                })
            else:
                # Add a slot if there's a gap between the last end time and the current start time
                if event.start_time > self.last_end_time:
                    if current_date not in self.available_slots_by_date:
                        self.available_slots_by_date[current_date] = []
                    self.available_slots_by_date[current_date].append({
                        'start_time': self.last_end_time.time().isoformat(),
                        'end_time': event.start_time.time().isoformat()
                    })

            self.last_end_time = max(self.last_end_time, event.end_time)

        # Add last available slot to the last event date
        last_date = self.last_end_time.date().isoformat()
        self.available_slots_by_date[last_date].append({
            'start_time': self.last_end_time.time().isoformat(),
            'end_time': end_of_day.isoformat()
        })

    def save_available_slots(self, file_path):
        FileHandler.save_to_file(self.available_slots_by_date, file_path)


if __name__ == "__main__":
    scheduler = EventScheduler()
    scheduler.load_events('./asset/events.json')
    scheduler.sort_events()
    scheduler.calculate_available_slots()
    scheduler.save_available_slots('./out/available_slots.json')
