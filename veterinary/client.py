class Client:

    def __init__(self, name, lastname):
        self.__name = name
        self.__lastname = lastname
        self.__client_id = None

    def get_id(self):
        return self.__client_id

    def get_name(self):
        return self.__name

    def get_lastname(self):
        return self.__lastname

    def set_id(self, id):
        self.__client_id = id
