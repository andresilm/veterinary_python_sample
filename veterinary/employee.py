class Employee:

    def __init__(self, name, lastname):
        self._name = name
        self._lastname = lastname
        self.__employee_id = None
        self.__working_days = dict()

    def set_working_day(self, day_nr, start_time, end_time):
        self.__working_days.update({day_nr: (start_time, end_time)})

    def get_name(self):
        return self._name

    def get_lastname(self):
        return self._lastname

    def get_id(self):
        return self.__employee_id

    def __eq__(self, other):
        return self._name == other._name and self._lastname == \
                                             other._lastname

    def works(self, day_nr, hour):
        return day_nr in self.__working_days and self.__working_days[
                                                     day_nr][1] >= hour >= \
                                                 self.__working_days[day_nr][0]

    def __str__(self):
        return self._lastname + ", " + self._name + ":" + str(
            self.__working_days)

    def set_id(self, id):
        self.__employee_id = id
