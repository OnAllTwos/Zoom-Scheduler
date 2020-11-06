import os
import threading
import datetime
from meeting import meeting

zoom_dir = "%APPDATA%/Zoom/bin/Zoom.exe"
def check_for_classes(schedule_dict):
#        os.system('start "" "%APPDATA%\\Zoom\\bin\\Zoom.exe" --url="zoommtg://zoom.us/join?action=join&confno=91233680892"')
    t = threading.currentThread()
    prev_day = None
    meetings_today = set()
    while getattr(t, "run", True):  #Checking for 
        today = datetime.date.today()
        day = today.strftime("%A").lower()
        for _meeting in meetings_today:
            if not _meeting.timedout:
                if day.time().strftime("%H:%M") == _meeting.time:
                    open_meeting(_meeting)

def set_zoom_dir(new_dir):
    global zoom_dir
    zoom_dir = new_dir

def open_meeting(meeting_to_open: meeting):
    os.system(f'start "" "%APPDATA%\\Zoom\\bin\\Zoom.exe" --url="zoommtg://zoom.us/join?action=join&confno={meeting_to_open.meeting_id}"')