import file_handler
import scheduler
import prompt
import threading

schedule_dict = {}
waiting = False
options = {0: ["Start scheduler", "Stop Scheduler"],
           1: ["Load schedule from file"],
           2: ["Add new entry to schedule"],
           3: ["Create new schedule file"],
           4: ["Change Zoom Directory"],
           5: ["View schedule"],
           6: ["Quit"]
           }


def print_schedule(sch):
    print('-' * 96)
    
    for day, meetings in sch.items():
        for meeting in meetings:
            print(f'| {day: <10} | {repr(meeting): <80}|')
    
    print('-' * 96)


def print_menu():
    print("---------------------------------")
    for num, option in options.items():
        print(f'| {num} - {option[1] if num == 0 and waiting else option[0]}'.ljust(32) + '|')
    print("---------------------------------")
    if waiting:
        print("Currently waiting for classes to start...")


if __name__ == "__main__":
    while True:
        print_menu()
        selection = prompt.for_int_between("Please select an option", 0, len(options)-1, default=0)
        if selection == 0:
            if not waiting:
                waiting = True
                waitThread = threading.Thread(target=scheduler.check_for_classes, args=[schedule_dict])
                waitThread.start()
                print("Now waiting for classes to start...")
            else:
                waitThread.run = False
                waiting = False
        elif selection == 1:
            schedule_dict = file_handler.read_schedule(file_handler.get_file())
            print("Successfully loaded schedule from file!")
        elif selection == 5:
            print_schedule(schedule_dict)
        elif selection == 6:
            break