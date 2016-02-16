class Pet:

    __exercise_message = "{name} {exercise_action} durante una hora"

    def __init__(self,name, weight, exercise_time):
        self.__name = name
        self.__weight = weight
        self.__exercise_time = exercise_time
        self.action = "se ejercitó"


    def do_exercise(self):
        print(self.__exercise_message.format(name=self.get_name(),
                                             exercise_action=self.action,
                                             hours=self.exercise_time()))

    def get_name(self):
        return self.__name

    def exercise_time(self):
        return self.__exercise_time

