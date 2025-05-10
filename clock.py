import time

class Clock:
    def __init__(self, time_limit, turn = None):
        self.time_limit = time_limit
        self.remaining_time = time_limit
        self.turn = turn
        self.start_time = None 
        self.end_time = None

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.remaining_time = max(0, self.remaining_time - elapsed)
            self.start_time = None

    def reset(self):
        self.remaining_time = self.time_limit
        self.start_time = None

    def is_running(self):
        return self.start_time is not None
    
    def time_record(self):#จับเวลาไปให้game_data
        if self.is_running():
            elapsed = time.time() - self.start_time
            return max(0, self.remaining_time - elapsed)
        return self.remaining_time
