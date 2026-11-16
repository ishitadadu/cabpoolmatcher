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


def is_ahead(a, b):
    if a.year != b.year:
        return a.year > b.year
    return a.request_id < b.request_id


def pick_most_senior(students, count):
    left = students.copy()
    picked = []
    while len(left) > 0 and len(picked) < count:
        best = left[0]
        for s in left:
            if is_ahead(s, best):
                best = s
        picked.append(best)
        left.remove(best)
    return picked


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
    print("\n=== Waiting students (most senior first) ===")
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
            for s in pick_most_senior(students, len(students)):
                print("  " + s.describe())

    print("\n=== Cabs ===")
    if len(cabs) == 0:
        print("No cabs loaded.")
    for cab in cabs:
        print(cab.describe())
        for p in cab.passengers:
            print("    - " + p.name + " (Year " + str(p.year) + ")")


def find_matches():
    print("\n=== Match preview (nothing changes) ===")
    already_shown = []
    for cab in cabs:
        if cab.has_left:
            continue
        candidates = []
        for s in students_for(cab.destination, cab.time_slot):
            if s not in already_shown:
                candidates.append(s)
        picks = pick_most_senior(candidates, cab.free_seats())
        for s in picks:
            already_shown.append(s)

        print("\n" + cab.driver + " -> " + cab.destination + ", " + cab.time_slot +
              " would take " + str(len(picks)) + "/" + str(cab.free_seats()) + ":")
        if len(picks) == 0:
            print("  nobody waiting for this trip")
        for s in picks:
            print("  - " + s.name + " (Year " + str(s.year) + ")")

    still_waiting = len(waiting) - len(already_shown)
    if still_waiting > 0:
        print("\n" + str(still_waiting) + " student(s) would still be waiting.")


def main():
    load_cabs()
    while True:
        print("\n----- Cab Pool Matcher -----")
        print("1. Add a ride request")
        print("2. View waiting students and all cabs")
        print("3. Find matches (preview)")
        print("4. Quit")
        choice = input("Choose 1-4: ").strip()
        if choice == "1":
            add_request()
        elif choice == "2":
            view_all()
        elif choice == "3":
            find_matches()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Please enter a number from 1 to 4.")


main()