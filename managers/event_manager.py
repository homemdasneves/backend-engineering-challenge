# from models import event
import numpy as np
from datetime import datetime, timedelta
import uuid
import jsonlines # https://jsonlines.readthedocs.io/
from models.event import Event

class EventManager:

    def calc_moving_average(self, file, window_size):

        # setup a data structures to gather data for each minute
        data_minutes = []
        data_aggregate_duration = []
        data_event_count = []
        data_averages = []
        last_processed_minute = datetime.max

        # iterate through the file, line by line
        with jsonlines.open(file, mode='r') as reader:
            for obj in reader:
                ev = Event(**obj)
                minute_rounded = ev.get_minute_rounded()
                minute_key = str(minute_rounded)

                # if there are a few seconds without events, 
                # add some records (with events=0 and duration=0)
                expected_last_minute = minute_rounded - timedelta(minutes=1)
                while last_processed_minute < expected_last_minute:
                    last_processed_minute += timedelta(minutes=1)
                    data_minutes.append(str(last_processed_minute))
                    data_aggregate_duration.append(0)
                    data_event_count.append(0)
                
                if minute_key in data_minutes:
                    i = data_minutes.index(minute_key)
                    data_aggregate_duration[i] += ev.duration
                    data_event_count[i] += 1
                else:
                    data_minutes.append(minute_key)
                    data_aggregate_duration.append(ev.duration)
                    data_event_count.append(1 if ev.duration > 0 else 0)

                last_processed_minute = minute_rounded

        # finally, calculate the averages
        for i in range(0, len(data_minutes)):
            slice_low_limit = i-window_size if i > window_size else 0
            slice_high_limit = i

            aggregate_duration_in_window = sum(data_aggregate_duration[slice_low_limit:slice_high_limit])
            event_count_in_window = sum(data_event_count[slice_low_limit:slice_high_limit]) 
            mov_avg = aggregate_duration_in_window / event_count_in_window if event_count_in_window > 0 else 0
            data_averages.append(mov_avg)

        output = list(
            map(
                lambda x: {
                    "date": data_minutes[x],
                    "average_delivery_time": data_averages[x]
                },
                range(0, len(data_minutes))
            )
        )

        self.save_json_file("output.txt", list(output))

        return output

    def save_json_file(self, file_name, json_list):
        with jsonlines.open(file_name, mode='w') as writer:
            writer.write_all(json_list)

    def generate_events(self, size, filename):

        # get random values from poisson distribution
        delays = np.random.poisson(lam=1, size=size)

        # aggregate delays
        agg_delays = np.cumsum(delays).tolist()

        dt = datetime.now()

        events = list(
            map(
                lambda x: dict(
                    timestamp = str(dt + timedelta(seconds = x)),
                    translation_id =  uuid.uuid4().hex,
                    source_language = "en",
                    target_language = "fr",
                    client_name = "easyjet",
                    event_name = "translation_delivered",
                    nr_words = int(np.random.randint(10, 100, 1)[0]),
                    duration = int(np.random.randint(10, 100, 1)[0])
                ),
                agg_delays
            )
        )

        self.save_json_file(filename, events)