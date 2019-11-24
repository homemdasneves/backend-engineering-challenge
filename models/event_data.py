import datetime

class EventData:
    
    def __init__(self, 
        aggregate_duration : int, 
        event_count : int):

        self.aggregate_duration = aggregate_duration
        self.event_count = event_count

