from random import randrange

cars = ["BMW", "VW", "Ford", "Mazda"]

kms = {car: randrange(100) for car in cars}

print(kms)

#Get BMW data
print(kms[cars[0]])