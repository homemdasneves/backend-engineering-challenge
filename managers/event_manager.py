import numpy as np
from datetime import datetime, timedelta
import uuid
import jsonlines # https://jsonlines.readthedocs.io/
from models.event import Event
from models.event_data import EventData

class EventStream:

    def __init__(self):
        self.data = dict() # data dictionary will gather data for each minute

    def add_event(self, ev : Event):

        minute_rounded = ev.timestamp.replace(second=0, microsecond=0)

        if minute_rounded in self.data.keys():
            ev_data = self.data[minute_rounded]
            ev_data.aggregate_duration += ev.duration
            ev_data.event_count += (1 if ev.duration > 0 else 0)
        else:
            self.data[minute_rounded] = EventData(ev.duration, 1 if ev.duration > 0 else 0)

        return minute_rounded

    def calc_moving_average(self, file : str, window_size : int):
        """ main method to perform the calculation of the moving average
        """

        try:

            # iterate through the file, line by line
            with jsonlines.open(file, mode="r") as reader:
                for obj in reader:
                    ev = Event(**obj)
                    self.add_event(ev)

            # finally, calculate the moving averages
            first_minute = min(self.data)
            last_minute = max(self.data)
            minutes_in_stream = int((last_minute-first_minute).seconds/60)
            all_minutes = [first_minute + timedelta(minutes=x) for x in range(0, minutes_in_stream+2)]

            output = []
            for minute in all_minutes:
                
                window_min = minute - timedelta(minutes=window_size)
                events_in_window = list(filter(lambda x: window_min <= x and x < minute, self.data.keys()))
                
                aggregate_duration_in_window = sum([self.data[e].aggregate_duration for e in events_in_window])
                event_count_in_window = sum([self.data[e].event_count for e in events_in_window])
                mov_avg = aggregate_duration_in_window / event_count_in_window if event_count_in_window > 0 else 0

                output.append({"date": str(minute), "average_delivery_time": mov_avg})

            self.save_json_file("output.txt", output)

            return f"Done!"

        except Exception as e:
            return f"An unexpected error ocurred ({str(e)})"

    @classmethod
    def save_json_file(cls, file_name : str, json_list : str):
        with jsonlines.open(file_name, mode="w") as writer:
            writer.write_all(json_list)

    @classmethod
    def generate_events(cls, size : int, lam : float, filename : str):

        # get random values from poisson distribution
        delays = np.random.poisson(lam=lam, size=size)

        # aggregate delays
        agg_delays = np.cumsum(delays).tolist()

        dt = datetime.now()

        events = list(
            map(
                lambda x: dict(
                    timestamp = str(dt + timedelta(minutes = x)),
                    duration = int(np.random.randint(10, 100, 1)[0])
                ),
                agg_delays
            )
        )

        cls.save_json_file(filename, events)