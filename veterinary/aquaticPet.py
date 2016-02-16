from veterinary.pet import Pet


class AquaticPet(Pet):
    def __init__(self, *args):
        super(AquaticPet, self).__init__(*args)

        self.action = "nadó"
