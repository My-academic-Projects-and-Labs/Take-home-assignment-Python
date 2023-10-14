from datetime import datetime
import json

# Encapsulation: Event, EventScheduler related attributes and behaviors
class Event:
    def __init__(self, start_time, end_time):
        self.start_time = datetime.fromisoformat(start_time)
        self.end_time = datetime.fromisoformat(end_time)


class EventScheduler:
    def __init__(self, initial_time):
        self.events = []
        self.last_end_time = datetime.fromisoformat(initial_time)
        self.available_slots_by_date = {}

    def load_events_from_file(self, file_path):
        with open(file_path, 'r') as f:
            events_data = json.load(f)
        self.events = [Event(event['start']['dateTime'], event['end']['dateTime']) for event in events_data]

    # Abstraction - Hiding the sorting logic and details of slot calculation within a method
    def sort_events(self):
        self.events.sort(key=lambda event: event.start_time)

    def calculate_available_slots(self):
        for event in self.events:
            start_time = event.start_time
            end_time = event.end_time

            if start_time > self.last_end_time:
                date_str = self.last_end_time.date().isoformat()
                if date_str not in self.available_slots_by_date:
                    self.available_slots_by_date[date_str] = []
                self.available_slots_by_date[date_str].append({
                    'start_time': self.last_end_time.time().isoformat(),
                    'end_time': start_time.time().isoformat()
                })

            self.last_end_time = max(self.last_end_time, end_time)

    def save_available_slots_to_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.available_slots_by_date, f, indent=2)


if __name__ == "__main__":
    scheduler = EventScheduler('2023-08-31T00:00:00+05:30')
    scheduler.load_events_from_file('./asset/events.json')
    scheduler.sort_events()
    scheduler.calculate_available_slots()
    scheduler.save_available_slots_to_file('./out/available_slots.json')
