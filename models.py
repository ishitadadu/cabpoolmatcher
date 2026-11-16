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
