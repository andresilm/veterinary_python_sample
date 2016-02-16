#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pickle

from veterinary.veterinary import Veterinary


class Application:
    def __init__(self, args):
        self.__load_from_file("veterinaria.sav")
        self.__turn_head = "Turno |    Fecha    |" \
                           " Inicio |  Fin |     Cliente     |    Encargado"
        self.__turn_printed = "{turn_id}\t{day}/{month}/{year}\t{s_hour}\t{" \
                              "e_hour}\t{" \
                              "client}\t{" \
                              "employee}\n"
        self.__days = ["lunes", "martes", "miercoles", "jueves", "viernes",
                       "sabado", "domingo"]

    def __load_from_file(self, filename):
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]

        if filename in onlyfiles:
            load_file = open(filename, "rb")
            self.__vet = pickle.load(load_file)
        else:
            self.__vet = Veterinary()

    def run(self):
        while True:
            self.display_menu()
            option = self.int_input("Escoja una opción\n")

            if option == 0:
                self.add_client()
            elif option == 1:
                self.add_employee()
            elif option == 2:
                self.new_appointment()
            elif option == 3:
                self.add_pet()
            elif option == 4:
                self.assign_pet()
            elif option == 5:
                self.print_pending_turns()
            elif option == 6:
                self.process_appointment()
            elif option == 7:
                self.quit()
            else:
                print("Escoja una opción entre 0 y 7")

    def add_client(self):
        name, lastname = (input("Ingrese nombre y apellido del "
                                "cliente:\n")).split(" ")
        while name == "" and lastname == "":
            print("Por favor ingrese nombre y apellido válidos")

        self.__vet.add_client(name, lastname)

    def add_employee(self):
        name, lastname = (input("Ingrese nombre y apellido del "
                                "empleado:\n")).split(" ")
        while name == "" or lastname == "":
            print("Por favor ingrese nombre y apellido válidos")

        employee = self.__vet.add_employee(name, lastname)

        print("A continuación cargue los horarios de trabajo, "
              "un día por línea. Escriba 'fin' en la última línea "
              "para finalizar")
        line = ""

        while line != "fin":
            line = input("Ingrese otro día laboral. "
                         "Ej: "
                         "'Lunes 9 "
                         "18'\n")
            if line != "fin":
                day, start_time, end_time = (line).split(" ")
                day_nr = self.__days.index(day.lower())
                print(day_nr)
                start_time = int(start_time)
                end_time = int(end_time)

                if self.__is_valid_date(day, start_time, end_time):
                    self.__vet.add_working_day_to_employee(employee.get_id(), day_nr,
                            start_time, end_time)
                else:
                    print("Día u horario no válido.")

    def __parse_timedate(self, input_date):
        import datetime
        fmt = '%d/%m/%Y %H'
        date = datetime.datetime.strptime(input_date, fmt)

        return date

    def __is_valid_date(self, day, start_time, end_time):
        return day in self.__days and 0 <= start_time <= end_time < 24


    def new_appointment(self):
        client_id = -1

        while not self.__vet.client_id_exists(client_id):
            client_id = self.int_input("Ingrese número de cliente:\n")

        datetime = input("Ingrese fecha y hora para el turno.Ej: 17/01/2016 15"
                         "\n")

        try:
            datetime = self.__parse_timedate(datetime)
        except Exception:
            print("Fecha u hora ingresado no es válido.")

        if datetime < datetime.today():
            print("Fecha u hora ingresado no es válido.")
        else:
            app_id = self.__vet.new_appointment(client_id, datetime.hour,
                                              datetime.day, datetime.month,
                                              datetime.year)
            if app_id >= 0:
                print("Hecho.")
            else:
                print("No se pudo asignar un turno para todas las mascotas a "
                      "un "
                      "empleado en la fecha y hora solicitados.")

    def int_input(self, message):
        num = None
        while num is None:
            try:
                num = int(input(message))
            except ValueError:
                print("Debe ingresar un número.")

        return num

    def add_pet(self):
        id = self.int_input("Ingrese el id del cliente dueño de la mascota\n")
        while not self.__vet.client_id_exists(id):
            id = self.int_input("Ingrese un id de cliente válido, dueño de la "
                                "mascota\n")

        name = input("Ingrese nombre de la mascota\n")

        type = self.int_input("Ingrese el tipo de mascota según "
                              "corresponda:\n"
                              "0:Terrestre \n"
                              "1:Anfibio\n"
                              "2:Acuático\n")

        weight = input("Ingrese el peso en gramos.\n")
        exerc_time = input("Señale la cantidad de tiempo que necesita "
                           "ejercitarse por día (en horas)\n")

        result = self.__vet.create_pet(int(id), name, type, int(weight),
                                       int(exerc_time))
        if result:
            print("Hecho.")
        else:
            print("Ocurrió un error al crear la entrada para la nueva "
                  "mascota.")

    def assign_pet(self):
        client_id = self.int_input("Ingrese id del cliente:\n")
        pet_id = self.int_input("Ingrese id de la mascota:\n")

        self.__vet.assign_pet(client_id, pet_id)

        print("Hecho.")

    def print_pending_turns(self):
        turns = self.__vet.list_appointments()
        if turns != []:
            print(self.__turn_head)
            for turn in turns:
                date = turn.get_date()
                client_id = turn.get_client()
                employee_id = turn.get_employee()
                client = self.__vet.get_client_by_id(client_id)
                employee = self.__vet.get_employee_by_id(employee_id)
                client_print = client.get_lastname() + ", " + client.get_name()
                employee_print = employee.get_lastname() + ', ' \
                    + employee.get_name()
                print(self.__turn_printed.format(day=date.day,
                                                 month=date.month,
                                                 year=date.year,
                                                 s_hour=date.hour,
                                                 e_hour=turn.end_time(),
                                                 client=client_print,
                                                 employee=employee_print,
                                                 turn_id=turn.get_id()))
        else:
            print("No hay turnos pendientes.")

    def process_appointment(self):
        turn_id = None

        turn_id = self.int_input("Ingrese id del turno:\n")

        err_code = self.__vet.process_appointment(turn_id)
        if err_code == 0:
            print("Hecho.")
        elif err_code == 1:
            print("El turno ingresado ya fue procesado con anterioridad.")
        elif err_code == 2:
            print("El turno ingresado no existe.")

    def quit(self):
        output_file = open("veterinaria.sav", "wb")
        print("Guardando cambios y saliendo.")
        pickle.dump(self.__vet, output_file)
        exit()

    def display_menu(self):
        print("0) Agregar cliente \n"
              "1) Agregar empleado \n"
              "2) Crear un turno \n"
              "3) Crear mascota \n"
              "4) Asignar mascota \n"
              "5) Listar turnos pendientes \n"
              "6) Atender turno \n"
              "7) Salir"
              )


if __name__ == "__main__":
    app = Application(sys.argv)
    app.run()
