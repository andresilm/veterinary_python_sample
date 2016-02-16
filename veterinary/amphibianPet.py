from veterinary.pet import Pet


class AmphibianPet(Pet):
    def __init__(self, *args):
        super(AmphibianPet, self).__init__(*args)

        self.action = "nadó y caminó"
