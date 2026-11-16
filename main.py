import json

from models import RideRequest, Cab, destinations, time_slots

cab_file = "cabs.json"

waiting = []
cabs = []
next_id = 1


def load_cabs():
    try:
        file = open(cab_file)
        data = json.load(file)
        file.close()
    except FileNotFoundError:
        print("Could not find " + cab_file + ". Starting with no cabs.")
        return
    except json.JSONDecodeError:
        print(cab_file + " is not valid JSON. Starting with no cabs.")
        return

    for item in data:
        driver = item.get("driver")
        seats = item.get("seats")
        destination = item.get("destination")
        time_slot = item.get("time_slot")

        if not driver:
            print("Skipping a cab with no driver name.")
        elif destination not in destinations:
            print("Skipping " + str(driver) + "'s cab: unknown destination.")
        elif time_slot not in time_slots:
            print("Skipping " + str(driver) + "'s cab: unknown time slot.")
        elif seats not in [1, 2, 3, 4]:
            print("Skipping " + str(driver) + "'s cab: seats must be 1 to 4.")
        else:
            cabs.append(Cab(driver, seats, destination, time_slot))

    print("Loaded " + str(len(cabs)) + " cab(s).")


def ask_name():
    while True:
        name = input("Student name: ").strip()
        if name != "":
            return name
        print("  Name can't be empty.")


def ask_choice(question, options):
    while True:
        answer = input(question + " " + str(options) + ": ").strip().capitalize()
        if answer in options:
            return answer
        print("  Sorry, please pick one of: " + ", ".join(options))


def ask_year():
    while True:
        answer = input("Year (1-5): ").strip()
        if answer in ["1", "2", "3", "4", "5"]:
            return int(answer)
        print("  Year must be a number from 1 to 5.")


def students_for(destination, time_slot):
    result = []
    for s in waiting:
        if s.destination == destination and s.time_slot == time_slot:
            result.append(s)
    return result


def find_open_cab(destination, time_slot):
    for cab in cabs:
        if cab.destination == destination and cab.time_slot == time_slot and not cab.has_left:
            return cab
    return None


def add_request():
    global next_id
    name = ask_name()
    destination = ask_choice("Destination", destinations)
    time_slot = ask_choice("Time slot", time_slots)
    year = ask_year()

    request = RideRequest(name, destination, time_slot, year, next_id)
    next_id = next_id + 1
    waiting.append(request)

    print("Added: " + request.describe())
    if find_open_cab(destination, time_slot) is None:
        print("Note: no open cab for " + destination + " " + time_slot +
              " right now. " + name + " stays on the waiting list.")


def view_all():
    print("\n=== Waiting students ===")
    if len(waiting) == 0:
        print("Nobody is waiting.")
    for destination in destinations:
        for time_slot in time_slots:
            students = students_for(destination, time_slot)
            if len(students) == 0:
                continue
            print("\n" + destination + ", " + time_slot + ":")
            if find_open_cab(destination, time_slot) is None:
                print("  (no open cab for this trip, students keep waiting)")
            for s in students:
                print("  " + s.describe())

    print("\n=== Cabs ===")
    if len(cabs) == 0:
        print("No cabs loaded.")
    for cab in cabs:
        print(cab.describe())
        for p in cab.passengers:
            print("    - " + p.name + " (Year " + str(p.year) + ")")


def main():
    load_cabs()
    while True:
        print("\n----- Cab Pool Matcher -----")
        print("1. Add a ride request")
        print("2. View waiting students and all cabs")
        print("3. Quit")
        choice = input("Choose 1-3: ").strip()
        if choice == "1":
            add_request()
        elif choice == "2":
            view_all()
        elif choice == "3":
            print("Bye!")
            break
        else:
            print("Please enter a number from 1 to 3.")


main()