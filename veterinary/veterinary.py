from veterinary.appointment import Appointment
from veterinary.client import Client
from veterinary.employee import Employee
from veterinary.petFactory import new_pet


class Veterinary:
    def __init__(self):
        self.__clients = dict()
        self.__employees = dict()
        self.__clients_pets = dict()
        # self.__pets = dict()
        self.__appointments = dict()

    def get_client_by_id(self, client_id):
        return self.__clients[client_id]

    def get_employee_by_id(self, employee_id):
        return self.__employees[employee_id]

    def add_client(self, name, lastname):
        id = -1
        client = Client(name, lastname)
        new_client = client not in [self.__clients[cid] for cid in
                                    self.__clients]
        if new_client:
            id = len(self.__clients)
            client.set_id(id)
            self.__clients.update({id: client})

        return id

    def number_of_clients(self):
        return len(self.__clients)

    def add_employee(self, name, lastname):

        employee = Employee(name, lastname)

        new_employee = employee not in [self.__employees[e] for e in
                                        self.__employees]

        if new_employee:
            eid = len(self.__employees)
            employee.set_id(eid)
            self.__employees.update({eid: employee})
        else:
            employee = None

        return employee

    def add_working_day_to_employee(self, employee_id, day_nr, start_time,
                                    end_time):

        self.__employees[employee_id].set_working_day(day_nr, start_time,
                                                      end_time)

    def new_appointment(self, client_id, hour, day, month, year):
        import random
        aid = -1
        candidates = self.search_available_employees(client_id, hour,
                                                     day, month, year)

        if len(candidates) > 0:
            employee_id = random.choice(candidates)
        else:
            employee_id = -1

        if employee_id >= 0:
            appnt = Appointment(client_id, self.__clients_pets[client_id],
                                hour,
                                day,
                                month,
                                year,
                                employee_id)

            aid = len(self.__appointments)
            appnt.set_id(aid)
            self.__appointments.update({aid: appnt})

        return aid

    def search_available_employees(self, client_id, start_time, day,
                                   month,
                                   year):
        import datetime

        candidates = []

        date = datetime.datetime(year, month, day)
        day_nr = date.weekday()

        for employee_id in self.__employees:
            if self.__employees[employee_id].works(day_nr, start_time):
                filter_function = (lambda t: t.is_pending() and
                                             t.get_employee() == employee_id and
                                             t.get_date().day == day and
                                             t.get_date().month == month and
                                             t.get_date().year == year)

                employee_tasks = list(
                    filter(filter_function, [self.__appointments[
                                                 appnt] for
                                             appnt in
                                             self.__appointments]))

                if employee_tasks == []:
                    candidates.append(employee_id)
                else:

                    duration = sum([pet.exercise_time()
                                    for pet in self.__clients_pets[
                                        client_id]])
                    end_time = start_time + duration
                    print("Duración del turno: " + str(duration) + " horas.")
                    is_busy = any(t.start_time() < start_time < t.end_time(

                    ) or
                                  t.start_time() < end_time < t.end_time()
                                  for t in employee_tasks)

                    if not is_busy:
                        candidates.append(employee_id)

        return candidates

    def create_pet(self, client_id, pet_name, pet_type, pet_weight,
                   hours_exercise):
        pet = new_pet(pet_name, pet_weight, pet_type,
                      hours_exercise)
        if pet is not None:
            # self.__pets.update({pet.get_id(): pet})
            self.assign_pet(client_id, pet)
            return True
        else:
            return False

    def assign_pet(self, client_id, pet):
        if client_id not in self.__clients_pets:
            self.__clients_pets.update({client_id: []})

        self.__clients_pets[client_id].append(pet)

    def list_appointments(self):
        # return sorted(self.__turns.items())
        return sorted(
            [self.__appointments[appnt] for appnt in self.__appointments if
             self.__appointments[appnt].is_pending()])

    def process_appointment(self, app_id):
        if app_id in self.__appointments:
            turn = self.__appointments[app_id]
            if turn.is_pending():

                pets = self.__clients_pets[turn.get_client()]

                for pet in pets:
                    for hour in range(pet.exercise_time()):
                        pet.do_exercise()

                turn.set_served()
                return 0
            else:
                return 1
        else:
            return 2

    def client_id_exists(self, id):
        return id in self.__clients

    def client_has_pets(self, client_id):
        return self.__clients_pets[client_id] is not []
