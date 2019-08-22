# Class to hold necessary information for booking a room for a single person

class Person:

    def __init__(self, time, first, last, email):
        self.time = time  # time: starting time for booking
        self.first = first  # first: first name of person
        self.last = last  # last: last name of person
        self.email = email  # email: @buffalo.edu email address of person
