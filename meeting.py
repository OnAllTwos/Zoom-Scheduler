import time

timeout_period = 30

class meeting():
    
    def __init__(self, days=[], time="0:00", meeting_id="0", name="", link=""):
        split_time = time.split(":")
        self.days = days
        self.time = time
        self.hours = int(split_time[0])
        self.minutes = int(split_time[1])
        self.name = name
        self.timedout = False
        self.meeting_id = meeting_id
        self.link = link
    
    def timeout(self):
        #Start this in a separate thread to keep the meeting from being started again for a period.
        self.acknowledged = True
        time.sleep(timeout_period)
        self.acknowledged = False
    
    def __repr__(self):
        return f"<MEETING for {self.name} [{self.meeting_id}] on {', '.join(self.days)} @ {self.time}>"

#    With some modification the class, this could be used to prohibit rebinding.
#     def __setattr__(self, name, value):
#         assert name not in self.__dict__, "Please only declare each attribute once."
#         self.__dict__[name] = value