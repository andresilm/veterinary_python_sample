import unittest
from veterinary.veterinary import Veterinary


class TestVeterinaryMethods(unittest.TestCase):
    def test_add_client(self):
        v = Veterinary()
        cid = v.add_client("name", "last_name")
        c = v.get_client_by_id(cid)
        self.assertTrue(cid >= 0 and c.get_name() == "name" and
                     c.get_lastname() == "last_name")

    def test_new_appointment_1(self):
        """
    tests new appointment with 2 different clients at same time and date,
    having two employees working
    """
        v = Veterinary()
        c0 = v.add_client("Andres", "Luna")
        c1 = v.add_client("Laura", "Misetich")

        e0 = v.add_employee("Alfredo", "Costas")
        v.add_working_day_to_employee(e0, 0, 9, 13)

        e1 = v.add_employee("Julia", "Rodriguez")
        v.add_working_day_to_employee(e1, 0, 9, 18)

        v.create_pet(c0, "kino", 0, 4000, 2)
        v.create_pet(c1, "bizcocho", 0, 3000, 3)

        aid0 = v.new_appointment(c0, 9, 7, 3, 2016)
        aid1 = v.new_appointment(c1, 9, 7, 3, 2016)

        self.assertTrue(aid0 >= 0)
        self.assertTrue(aid1 >= 0)

        apps = v.list_appointments()

        self.assertTrue(len(apps) == 2)
        self.assertTrue(apps[0].get_employee() != apps[1].get_employee())
        self.assertTrue(
            apps[0].end_time() - apps[0].start_time() == 2)
        self.assertTrue(apps[1].end_time() - apps[1].start_time() == 3)


unittest.main()
