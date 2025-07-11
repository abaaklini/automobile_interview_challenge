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

        # Marca
        brand = get_user_input("Qual marca de carro você procura? (Ex: Toyota, Ford, Chevrolet, qualquer) ")
        if brand and brand.lower() not in ["qualquer", "tanto faz"]:
            filters["marca"] = brand.title()

        # Modelo
        model = get_user_input("Tem algum modelo específico em mente? (ou pressione ENTER para pular) ")
        if model:
            filters["modelo"] = model.title()

        # Ano
        year = get_user_input("Qual o ano mínimo desejado? (ou pressione ENTER para pular) ")
        if year:
            if year.isdigit() and 1900 <= int(year) <= 2100:
                filters["ano"] = int(year)
            elif year:
                print("Ano inválido. Informe um valor entre 1900 e 2100 ou deixe em branco.")

        # Tipo de combustível
        fuel_options = ["Gasolina", "Etanol", "Diesel", "Flex", "qualquer", ""]
        fuel_type = get_user_input(
            "Prefere algum tipo de combustível? (Gasolina, Etanol, Diesel, Flex, qualquer) ",
            options=fuel_options
        )
        if fuel_type and fuel_type.lower() not in ["qualquer", "tanto faz"]:
            filters["combustível"] = fuel_type.title()

        # Cor
        color = get_user_input("Cor preferida? (ou pressione ENTER para pular) ")
        if color:
            filters["cor"] = color.title()

        # Transmissão
        transmission_options = ["Manual", "Automático", "tanto faz", ""]
        transmission = get_user_input(
            "Prefere câmbio manual ou automático? (Manual, Automático, tanto faz) ",
            options=transmission_options
        )
        if transmission and transmission.lower() not in ["tanto faz"]:
            filters["transmissão"] = transmission.title()

        # Faixa de preço
        min_price = get_user_input("Qual o valor mínimo (em reais)? (ou pressione ENTER para pular) ")
        if min_price:
            if min_price.replace('.', '', 1).isdigit() and float(min_price) >= 0:
                filters["preço_minimo"] = float(min_price)
            else:
                print("Valor mínimo inválido. Informe um número positivo ou deixe em branco.")
        max_price = get_user_input("Qual o valor máximo (em reais)? (ou pressione ENTER para pular) ")
        if max_price:
            if max_price.replace('.', '', 1).isdigit() and float(max_price) >= 0:
                filters["preço_maximo"] = float(max_price)
            else:
                print("Valor máximo inválido. Informe um número positivo ou deixe em branco.")

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

# Exemplo de uso:
if __name__ == "__main__":
    filters = collect_filters()
    # Aqui você pode seguir para enviar os filtros ao servidor!