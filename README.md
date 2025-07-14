# Automobile Interview Challenge

A Python client-server application for searching vehicles in a database using customizable filters. This project demonstrates socket programming, database operations with SQLAlchemy, and interactive CLI interfaces.

## Features

- **Client-Server Architecture**: Socket-based communication between client and server
- **Interactive Search**: User-friendly CLI interface with Portuguese prompts
- **Flexible Filtering**: Search by brand, model, year, fuel type, color, transmission, engine, doors, and price
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **Testing Suite**: Unit and integration tests with pytest

## Project Structure

```
automobile_interview_challenge/
├── client.py           # Client application with interactive interface
├── server.py           # Server handling search requests
├── models.py           # Database models and SQLAlchemy configuration
├── populate.py         # Database population script
├── requirements.txt    # Python dependencies
├── test_client.py      # Unit tests for client functionality
├── test_integration.py # Integration tests for client-server communication
└── database.db        # SQLite database (generated)
```

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd automobile_interview_challenge
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with the following default values:

```
DATABASE_URL=sqlite:///database.db
SERVER_HOST=127.0.0.1
SERVER_PORT=65432
HOST=0.0.0.0
```

## Database Setup

### 5. Populate the database

This will create the SQLite database and insert sample car data:

```bash
python populate.py
```

## Running the Application

### 6. Start the server

```bash
python server.py
```

The server will start listening on `127.0.0.1:65432` by default.

### 7. Run the client

Open a new terminal and run:

```bash
python client.py
```

Follow the interactive prompts to search for vehicles using various filters.

## Testing

### Run all tests

```bash
pytest
```

### Run specific test files

```bash
python -m unittest test_client.py
python -m unittest test_integration.py
```

## Usage Example

When you run the client, you'll see an interactive interface in Portuguese:

```
==================================================
Bem-vindo ao Assistente Virtual de Busca de Veículos!
Vou fazer algumas perguntas para te ajudar a encontrar o carro ideal.

Qual marca de carro você procura? (Ex: Toyota, Ford, Chevrolet, qualquer) Toyota
Tem algum modelo específico em mente? (ou pressione ENTER para pular) Corolla
Qual o ano mínimo desejado? (ou pressione ENTER para pular) 2020
...
```

## Filter Options

The application supports the following search filters:

- **Marca (Brand)**: Toyota, Ford, Chevrolet, etc.
- **Modelo (Model)**: Corolla, Fiesta, Onix, etc.
- **Ano (Year)**: Minimum year (1900-2100)
- **Combustível (Fuel Type)**: Gasolina, Etanol, Diesel, Flex
- **Cor (Color)**: Branco, Preto, Prata, etc.
- **Transmissão (Transmission)**: Manual, Automático
- **Motor (Engine)**: Engine specifications
- **Portas (Doors)**: Number of doors
- **Preço (Price)**: Minimum and maximum price range

## Technical Details

- **Language**: Python 3.x
- **Database**: SQLite with SQLAlchemy ORM
- **Communication**: TCP sockets with JSON message format
- **Testing**: pytest framework
- **Environment**: python-dotenv for configuration

## Notes

- The database file (`database.db`) and environment file (`.env`) are ignored by git
- Make sure the server is running before starting the client
- You can adjust the number of cars generated in `populate.py` by changing `NUM_CARS_TO_GENERATE`
- The application uses Portuguese language for user interface to demonstrate localization

## Dependencies

- `SQLAlchemy`: Database ORM
- `python-dotenv`: Environment variable management
- `pytest`: Testing framework
- `greenlet`: SQLAlchemy dependency for async support

## License

This project is for educational/interview purposes.