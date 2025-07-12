import os
import socket
import json
from dotenv import load_dotenv

load_dotenv()

def get_user_input(prompt, options=None, allow_empty=True):
    """
    Requests user input, validates options and required field.
    """
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("Esse campo não pode ser vazio. Tente novamente.")
            continue
        if options and value and value.lower() not in [opt.lower() for opt in options]:
            print(f"Opções válidas: {', '.join(options)}")
            continue
        return value

def collect_filters():
    """
    Collects vehicle search filters from the user.
    """
    while True:
        print("=" * 50)
        print("Bem-vindo ao Assistente Virtual de Busca de Veículos!")
        print("Vou fazer algumas perguntas para te ajudar a encontrar o carro ideal.\n")
        filters = {}

        brand = get_user_input("Qual marca de carro você procura? (Ex: Toyota, Ford, Chevrolet, qualquer) ")
        if brand and brand.lower() not in ["qualquer", "tanto faz"]:
            filters["marca"] = brand.title()

        model = get_user_input("Tem algum modelo específico em mente? (ou pressione ENTER para pular) ")
        if model:
            filters["modelo"] = model.title()

        year = get_user_input("Qual o ano mínimo desejado? (ou pressione ENTER para pular) ")
        if year:
            if year.isdigit() and 1900 <= int(year) <= 2100:
                filters["ano"] = int(year)
            elif year:
                print("Ano inválido. Informe um valor entre 1900 e 2100 ou deixe em branco.")

        fuel_options = ["Gasolina", "Etanol", "Diesel", "Flex", "qualquer", ""]
        fuel_type = get_user_input(
            "Prefere algum tipo de combustível? (Gasolina, Etanol, Diesel, Flex, qualquer) ",
            options=fuel_options
        )
        if fuel_type and fuel_type.lower() not in ["qualquer", "tanto faz"]:
            filters["combustível"] = fuel_type.title()

        color = get_user_input("Cor preferida? (ou pressione ENTER para pular) ")
        if color:
            filters["cor"] = color.title()

        transmission_options = ["Manual", "Automático", "tanto faz", ""]
        transmission = get_user_input(
            "Prefere câmbio manual ou automático? (Manual, Automático, tanto faz) ",
            options=transmission_options
        )
        if transmission and transmission.lower() not in ["tanto faz"]:
            filters["transmissão"] = transmission.title()

        min_price = get_user_input("Qual o valor mínimo (em reais)? (ou pressione ENTER para pular) ")
        if min_price:
            if min_price.replace('.', '', 1).isdigit() and float(min_price) >= 0:
                filters["preço_mínimo"] = float(min_price)
            else:
                print("Valor mínimo inválido. Informe um número positivo ou deixe em branco.")

        max_price = get_user_input("Qual o valor máximo (em reais)? (ou pressione ENTER para pular) ")
        if max_price:
            if max_price.replace('.', '', 1).isdigit() and float(max_price) >= 0:
                filters["preço_máximo"] = float(max_price)
            else:
                print("Valor máximo inválido. Informe um número positivo ou deixe em branco.")

        engine_options = ["1.0", "1.4", "1.6", "1.8", "2.0", "2.4", "qualquer", ""]
        engine = get_user_input(
            "Qual o tamanho do motor? (1.0, 1.4, 1.6, 1.8, 2.0, 2.4, qualquer) ",
            options=engine_options
        )
        if engine and engine.lower() not in ["qualquer", "tanto faz"]:
            filters["motor"] = engine.title()

        doors_options = ["2", "4", "tanto faz", ""]
        doors = get_user_input(
            "Quantas portas? (2, 4, tanto faz) ",
            options=doors_options
        )
        if doors and doors.lower() not in ["tanto faz"]:
            if doors in ["2", "4"]:
                filters["portas"] = int(doors)
            else:
                print("Opção inválida. Informe 2, 4 ou deixe em branco.")

        mileage = get_user_input("Qual a quilometragem máxima desejada? (em km, ou pressione ENTER para pular) ")
        if mileage:
            if mileage.isdigit() and int(mileage) >= 0:
                filters["quilometragem"] = int(mileage)
            else:
                print("Quilometragem inválida. Informe um número positivo ou deixe em branco.") 

        print("\nResumo da sua busca:")
        for k, v in filters.items():
            print(f"{k.capitalize()}: {v}")

        confirm = get_user_input("Deseja continuar com esses filtros? (S/N) ", options=["S", "N", "s", "n"], allow_empty=False)
        if confirm.upper() == "N":
            print("Vamos tentar novamente.\n")
            continue
        else:
            print("Ótimo! Procurando veículos para você...\n")
            return filters

def send_filters_to_server(filters):
    host = os.getenv("SERVER_HOST")
    port = int(os.getenv("SERVER_PORT"))
    if not host or not port:
        print("SERVER_HOST or SERVER_PORT environment variable not set.")
        return None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((host, port))
            message = json.dumps(filters).encode('utf-8')
            s.sendall(message)
            data = s.recv(4096)
            try:
                response = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                print("Erro ao decodificar resposta do servidor.")
                return None
            return response
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Certifique-se que o servidor está rodando.")
        return None

if __name__ == "__main__":
    filters = collect_filters()
    results = send_filters_to_server(filters)
    if results is not None:
        print("=== Veículos encontrados ===")
        if not results:
            print("Nenhum veículo encontrado com os filtros fornecidos.")
        else:
            for car in results:
                print(
                    f"Marca: {car.get('brand')}, Modelo: {car.get('model')}, "
                    f"Ano: {car.get('year')}, Cor: {car.get('color')}, "
                    f"Quilometragem: {car.get('mileage')} km, "
                    f"Preço: R${car.get('price')}, "
                    f"Combustível: {car.get('fuel_type')}, "
                    f"Transmissão: {car.get('transmission')}, "
                    f"Portas: {car.get('doors')}, Motor: {car.get('engine')}, "
                    f"Placa: {car.get('license_plate')}"
                )