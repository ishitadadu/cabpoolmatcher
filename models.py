from datetime import datetime

destinations = ["Delhi", "Jaipur"]
time_slots = ["Morning", "Afternoon", "Evening", "Night"]


class RideRequest:
    def __init__(self, name, destination, time_slot, year, request_id):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.request_id = request_id
        self.submitted_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def describe(self):
        return "#" + str(self.request_id) + " " + self.name + ", Year " + str(self.year) + \
               " (asked at " + self.submitted_at + ")"
class Cab:
    def __init__(self, driver, seats, destination, time_slot):
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []

    def free_seats(self):
        return self.seats - len(self.passengers)

    def describe(self):
        if self.has_left:
            status = "LEFT"
        else:
            status = "open"
        taken = str(len(self.passengers)) + "/" + str(self.seats)
        return self.driver + " -> " + self.destination + ", " + self.time_slot + \
               ", seats " + taken + " [" + status + "]"


