import os
import socket
import json
from models import SessionLocal, Car
from dotenv import load_dotenv
from sqlalchemy import and_

load_dotenv()

def process_filters(filters):
    """
    Applies the filters received from the client to the database query.
    """
    FILTER_MAP = {
        "marca": "brand",
        "modelo": "model",
        "ano": "year",
        "combustível": "fuel_type",
        "cor": "color",
        "transmissão": "transmission",
        "motor": "engine",
        "portas": "doors",
        "combustível": "fuel_type"
    }

    with SessionLocal() as session:
        query = session.query(Car)

        # Exact filters
        for filtro_cliente, atributo_modelo in FILTER_MAP.items():
            valor = filters.get(filtro_cliente)
            if valor:
                # If it's a string, normalize for comparison
                if isinstance(valor, str):
                    valor = valor.strip()
                query = query.filter(getattr(Car, atributo_modelo) == valor)

        # Minimum year
        if filters.get("ano"):
            try:
                ano = int(filters["ano"])
                query = query.filter(Car.year >= ano)
            except ValueError:
                pass  # ignore if year is not valid

        # Minimum price
        if filters.get("preço_mínimo") is not None:
            try:
                min_price = float(filters["preço_mínimo"])
                query = query.filter(Car.price >= min_price)
            except ValueError:
                pass

        # Maximum price
        if filters.get("preço_máximo") is not None:
            try:
                max_price = float(filters["preço_máximo"])
                query = query.filter(Car.price <= max_price)
            except ValueError:
                pass
        
        # Fuel type and doors
        if filters.get("combustível"):
            fuel_type = filters["combustível"].title()
            query = query.filter(Car.fuel_type == fuel_type)

        if filters.get("portas"):
            doors = filters["portas"]
            query = query.filter(Car.doors == doors)
        
        # Mileage
        if filters.get("quilometragem"):
            mileage = filters["quilometragem"]
            query = query.filter(Car.mileage <= mileage)

        # Executes the query (for example, returns up to 15 vehicles)
        cars = query.limit(15).all()

        results = []
        for car in cars:
            results.append({
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "color": car.color,
                "mileage": car.mileage,
                "price": float(car.price),
                "fuel_type": car.fuel_type,
                "transmission": car.transmission,
                "doors": car.doors,
                "engine": car.engine,
                "license_plate": car.license_plate
            })
        return results

def start_server():
    host = os.getenv("HOST")
    port = int(os.getenv("SERVER_PORT"))

    print(f"Server listening on {host}:{port} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection received from {addr}")
                data = conn.recv(4096)
                if not data:
                    continue
                try:
                    filters = json.loads(data.decode('utf-8'))
                except Exception as e:
                    print(f"Error decoding filters: {e}")
                    conn.sendall(json.dumps([]).encode('utf-8'))
                    continue
                results = process_filters(filters)
                response = json.dumps(results).encode('utf-8')
                conn.sendall(response)
                print(f"Response sent to {addr}")

if __name__ == "__main__":
    start_server()
