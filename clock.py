class Clock:
    def __init__(self, time_limit, turn = None):
        self.time_limit = time_limit
        self.remaining_time = time_limit
        self.turn = turn
        self.start_time = None 
        self.end_time = None

    def start(self):
        pass

    def stop(self):
        pass

    def reset(self):
        pass

    def is_running(self):
        return False
    
    def time_record(self):#จับเวลาไปให้game_data
        pass
