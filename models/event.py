import datetime

class Event:
    
    def __init__(self, 
        timestamp : str, 
        translation_id : str = "", 
        source_language : str = "", 
        target_language : str = "", 
        client_name : str = "", 
        event_name: str = "", 
        nr_words : int = 0, 
        duration : int = 0):

        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        self.translation_id = translation_id
        self.source_language = source_language
        self.target_language = target_language
        self.client_name = client_name
        self.event_name = event_name
        self.nr_words = nr_words
        self.duration = duration

