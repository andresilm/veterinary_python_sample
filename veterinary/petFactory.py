from veterinary.terrestrialPet import TerrestrialPet
from veterinary.aquaticPet import AquaticPet
from veterinary.amphibianPet import AmphibianPet


def new_pet(name, weight, pet_type, exercise_time):
    if pet_type == 0:
        pet = TerrestrialPet(name, weight, exercise_time)
    elif pet_type == 2:
        pet = AquaticPet(name, weight, exercise_time)
    elif pet_type == 1:
        pet = AmphibianPet(name, weight, exercise_time)
    else:
        pet = None

    return pet
