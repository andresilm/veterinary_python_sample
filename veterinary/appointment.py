import datetime


class Appointment:

    def __init__(self, client, pets, hour, day, month, year, employee):
        self.__employee = employee
        self.__client = client
        self.__hour = hour
        self._date = datetime.datetime(year, month, day, hour)
        self.__pending = True
        self.__end_time = sum([pet.exercise_time() for pet in pets]) + hour
        self.__pets = pets.copy()

    def set_served(self):
        self.__pending = False

    def is_pending(self):
        return self.__pending

    def get_id(self):
        return self.__app_id

    def set_id(self, id):
        self.__app_id = id

    def get_client(self):
        return self.__client

    def get_employee(self):
        return self.__employee

    def get_date(self):
        return self._date

    def pets(self):
        return self.__pets

    def start_time(self):
        return self._date.hour

    def end_time(self):
        return self.__end_time

    def __lt__(self, other):
        return self._date.day < other._date.day and \
               self._date.month < other._date.month and \
               self._date.year < other._date.year
