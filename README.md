# Cab Pool Matcher

A command-line app for the end-of-semester rush. Students ask for a cab to Delhi or Jaipur, wait in a line for their trip, and get seats only when a cab is sent off. When seats are short, seniors go first.

Built for SUTT Back-End recruitment, Task 1. It uses only Python's standard library, so there is nothing to install.

## How to run

```
python3 main.py
```

You need Python 3. Everything is kept in memory, so closing the app starts fresh next time.

## Menu

1. Add a ride request: asks for name, destination, time slot and year, then adds the student to the waiting list.
2. View: shows everyone waiting (most senior first, grouped by trip) and every cab, open or left, with its passengers.
3. Find matches: shows who each open cab would take if it left now. Nothing changes.
4. Dispatch a cab: pick a destination and time slot. The first open cab for that trip takes the most senior students and leaves.
5. Quit: exits the app.

Bad input (a city we don't serve, a time slot that doesn't exist, "Year 7", an empty name) shows a message and asks again instead of crashing. Typing delhi or DELHI works too.

## Files

- main.py: the menu and all the app logic
- models.py: the two classes, RideRequest and Cab
- cabs.json: the list of cabs the app starts with

## The cab file

cabs.json is a list with one entry per cab:

```
[
  {"driver": "Ramesh", "seats": 4, "destination": "Delhi",  "time_slot": "Morning"},
  {"driver": "Vikram", "seats": 2, "destination": "Jaipur", "time_slot": "Afternoon"}
]
```

- seats must be 1 to 4.
- destination must be Delhi or Jaipur.
- time_slot must be Morning, Afternoon, Evening or Night.
- A bad entry is skipped with a message, and the rest still load.
- If the file is missing, the app starts with no cabs. Students can still be added and will wait.
- Cabs are always gone through in the order they appear in the file, so the app gives the same result every time.

## How seniority works

All waiting students are kept in one plain list called waiting. Every student gets a request_id: 1, 2, 3 and so on, in the order they asked.

To decide who goes first, is_ahead(a, b) compares two students. A higher year goes first. If the year is the same, the smaller request_id goes first, because they asked earlier.

pick_most_senior(students, count) loops through the list, finds the best student, takes them out of a copy of the list, and repeats until it has count students. Find Matches and Dispatch both use this same function, so the preview always matches exactly who Dispatch would take.

The task suggests a heap. I used a plain list with a loop because I fully understand it and can explain every line. With up to about 1,000 students the loop is instant, so a heap would only matter for much bigger numbers.

## Tricky situations

### 1. Half-empty cab

Any open cab can be sent off even if it won't be full. It takes whoever is waiting, up to its number of seats, and leaves. The app shows something like "3/4 seats filled" and "(1 seat(s) went empty)", and View keeps showing 3/4. Once a cab has left, it's never picked again, so nobody can be added to it.

If nobody is waiting for that trip, Dispatch says so and changes nothing, because sending an empty cab is almost certainly a mistake.

### 2. No cabs left

Students are never attached to a cab until it actually leaves. They stay in the waiting list. If there's no open cab for a trip, adding a request still works but shows a note, Dispatch says "No open cab for Jaipur Night. Nothing changed.", View marks that trip as having no open cab, and Find Matches says how many students would still be waiting.

The only place a student is removed from the waiting list is inside Dispatch, right after they're put in a cab. So nobody ever disappears.

### 3. Same year: who asked first

Every request gets the next request_id. When two students are in the same year, is_ahead gives the seat to the smaller id, the one who asked first.

I used a counter instead of the time they asked, because two students can ask in the same second. The time is stored only for display.

I tested this by adding three 3rd years and dispatching. They left in the order they asked.

### 4. Lots of students (1,000 waiting)

Here n is the number of students waiting (up to 1,000) and c is the number of cabs.

- Adding one request is O(1), because it just appends to the end of the list.
- Adding all 1,000 is O(n): 1,000 appends at O(1) each.
- Sending off one cab is O(n). Each of the up to 4 picks loops through the list once, and 4 times n is still O(n). Removing a student from the list is also O(n).
- Finding an open cab for a trip is O(c), because it loops through the cabs until it finds an open one. There are only a few cabs.
