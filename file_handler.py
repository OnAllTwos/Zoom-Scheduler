import prompt
import re
from collections import defaultdict
from os import path
import time
from meeting import meeting


class DayTimeError(Exception):
    
    def __init__(self, _file, _line_num, _ex_txt):
        self.file = _file
        self.line_num = _line_num
        self.ex_txt = _ex_txt
        self.message = "Invalid day/time format in file " + self.file + " on line " + str(self.line_num) + ": " + str(self.ex_txt)
        super().__init__(self.message)


def get_file() -> str:
    f_name = prompt.for_string("Please enter a path for a data file", default="testSchedule.txt")
    if path.exists(f_name):
        if f_name.endswith(".txt"):
            return f_name
        else:
            print("Invalid file type; Please use a .txt file")
    else:
        print("Invalid file location; Please enter a different directory")


def read_schedule(file: str) -> defaultdict(lambda: set()):
    # Maybe should throw an error if more than one of the same criteria is made for each meeting?
    # Currently, a second declaration will simply overwrite the first rather than throwing an error.
    # Could use the __setattr__ method in the class to prohibit rebinding if desired.
    time_check = re.compile("^(1[0-2]|[0-9])(?::([0-6][0-9]))?(am|pm)$")
    scheduleDict = defaultdict(lambda: set())
    with open(file) as f:
        meeting_to_add = meeting()
        for num, line in enumerate(f, 1):
            # This is the primary file data handler. This takes file info and makes a dictionary with sets of days as keys
            # and meeting objects as values.
            data_type = line.lower().split(":")[0]
            
            if data_type == "days":
                for day in meeting_to_add.days:     #Before resetting the meeting, add it to the dict
                    scheduleDict[day].add(meeting_to_add)
                meeting_to_add = meeting()          #Reset the meeting since the "Day" term marks a new class listing.
                try:
                    days = line.strip().split(":")[1]
                    days_list = days.replace(" ", "").split(",")
                except IndexError:
                    raise DayTimeError(file, num, "No days entered")
                if all([True if day.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] else False for day in days_list]):
                    meeting_to_add.days = days_list
                else:
                    raise DayTimeError(file, num, days)     #Make sure that all the days are actually valid.
            
            if data_type == "time":
                time_raw = ":".join(line.strip().replace(" ", "").split(":")[1:])
                if match := time_check.match(time_raw):
                    hours, minutes, ampm = match.groups()
                    if not minutes:
                        minutes = "00"
                else:
                    raise DayTimeError(file, num, time_raw)
                military_time = str((12 * ((ampm.lower() == "pm" and hours != "12") or (ampm.lower() == "am" and hours == "12")) + int(hours)) % 24)  + ":" + minutes  #Convert to military time to standardize
                meeting_to_add.time = military_time
            
            if data_type == "name":
                meeting_to_add.name = line.split(":")[1].strip()
            
            if data_type == "meeting id":
                meeting_id = line.split(":")[1].strip()
                assert meeting_id.isnumeric() and 9 <= len(meeting_id) <= 11, "Meeting ID must be numeric with 9 to 11 digits."     #Brief verification, to be improved
                meeting_to_add.meeting_id = line.split(":")[1].strip()
            
            if data_type == "link":
                meeting_to_add.link = line.split(":")[1].strip
            
        for day in meeting_to_add.days:         #Add the final meeting after having read every line
            scheduleDict[day].add(meeting_to_add)
    return scheduleDict

if __name__ == "__main__":
    print(read_schedule(get_file()))