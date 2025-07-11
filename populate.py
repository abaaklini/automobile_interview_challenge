import random
from models import Base, engine, SessionLocal, Car
from typing import Set

NUM_CARS_TO_GENERATE = 100
YEAR_RANGE = (2005, 2023)
PRICE_RANGE_BRL = (20000, 150000)
MILEAGE_RANGE = (0, 200000)

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
fuel_types = ["Gasolina", "Etanol", "Diesel", "Flex"]
colors = ["Branco", "Preto", "Cinza", "Prata", "Vermelho", "Azul"]
transmissions = ["Manual", "Automático"]
doors_options = [2, 4]

Base.metadata.create_all(bind=engine)

def generate_unique_license_plates(n: int) -> Set[str]:
    """Generates a set of unique license plates to avoid database constraint errors."""
    plates = set()
    while len(plates) < n:
        plates.add(random_license_plate())
    return plates


def random_license_plate() -> str:
    letters = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    number = str(random.randint(0, 9))
    middle_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    last_numbers = str(random.randint(0, 99)).zfill(2)
    return f"{letters}{number}{middle_letter}{last_numbers}"

def populate_database(n: int = NUM_CARS_TO_GENERATE):

    session = SessionLocal()
    cars = []
    unique_plates = generate_unique_license_plates(n)

    for license_plate in unique_plates:
        brand = random.choice(list(brands_and_models.keys()))
        model = random.choice(brands_and_models[brand])
        year = random.randint(*YEAR_RANGE)
        engine = random.choice(engines)
        fuel_type = random.choice(fuel_types)
        color = random.choice(colors)
        mileage = random.randint(*MILEAGE_RANGE)
        doors = random.choice(doors_options)
        transmission = random.choice(transmissions)
        price = round(random.uniform(*PRICE_RANGE_BRL), 2)

        cars.append(Car(
            brand=brand, model=model, year=year, engine=engine,
            fuel_type=fuel_type, color=color, mileage=mileage, doors=doors,
            transmission=transmission, price=price, license_plate=license_plate
        ))

    with SessionLocal() as session:
        session.bulk_save_objects(cars)
        session.commit()

    print(f"Successfully inserted {len(cars)} cars into the database.")

if __name__ == "__main__":
    populate_database()
