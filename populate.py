from faker import Faker
import random

from models import Base, engine, SessionLocal, Car

fake = Faker()

brands_and_models = {
    "Ford": ["Fiesta", "Focus", "Ka", "EcoSport"],
    "Toyota": ["Corolla", "Yaris", "Hilux", "Etios"],
    "Chevrolet": ["Onix", "Prisma", "S10", "Cruze"],
    "Volkswagen": ["Gol", "Polo", "Virtus", "T-Cross"],
    "Fiat": ["Uno", "Palio", "Argo", "Toro"],
    "Honda": ["Civic", "Fit", "HR-V", "City"],
    "Hyundai": ["HB20", "Creta", "Tucson", "Azera"]
}
engines = ["1.0", "1.4", "1.6", "1.8", "2.0", "2.4"]
fuel_types = ["Gasoline", "Ethanol", "Diesel", "Flex"]
colors = ["White", "Black", "Gray", "Silver", "Red", "Blue"]
transmissions = ["Manual", "Automatic"]
doors_options = [2, 4]

Base.metadata.create_all(bind=engine)

def random_license_plate():
    letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    number = str(random.randint(0, 9))
    middle_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    last_numbers = str(random.randint(0, 99)).zfill(2)
    return f"{letters}{number}{middle_letter}{last_numbers}"

def populate_database(n=100):
    session = SessionLocal()
    cars = []
    for _ in range(n):
        brand = random.choice(list(brands_and_models.keys()))
        model = random.choice(brands_and_models[brand])
        year = random.randint(2005, 2023)
        engine = random.choice(engines)
        fuel_type = random.choice(fuel_types)
        color = random.choice(colors)
        mileage = random.randint(0, 200_000)
        doors = random.choice(doors_options)
        transmission = random.choice(transmissions)
        price = round(random.uniform(20000, 150000), 2)
        license_plate = random_license_plate()
        
        car = Car(
            brand=brand,
            model=model,
            year=year,
            engine=engine,
            fuel_type=fuel_type,
            color=color,
            mileage=mileage,
            doors=doors,
            transmission=transmission,
            price=price,
            license_plate=license_plate
        )
        cars.append(car)
    session.bulk_save_objects(cars)
    session.commit()
    session.close()
    print(f"Inserted {n} cars into the database.")

if __name__ == "__main__":
    populate_database()
