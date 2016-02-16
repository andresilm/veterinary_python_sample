from veterinary.pet import Pet


class TerrestrialPet(Pet):
    def __init__(self, *args):
        super(TerrestrialPet, self).__init__(*args)
        self.action = "caminó"
