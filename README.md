# Automobile Interview Challenge

A Python client-server application for searching vehicles in a database using customizable filters.

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd automobile_interview_challenge
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit the `.env` file if needed. Default values:

```
DATABASE_URL=sqlite:///database.db
SERVER_HOST=127.0.0.1
SERVER_PORT=65432
HOST=0.0.0.0
```

## Database

### 5. Populate the database

This will create the SQLite database and insert sample car data.

```bash
python populate.py
```

## Running

### 6. Start the server

```bash
python server.py
```

### 7. Run the client

Open a new terminal and run:

```bash
python client.py
```

Follow the prompts to search for vehicles.

## Testing

### 8. Run unit and integration tests

```bash
pytest
```
or
```bash
python -m unittest test_client.py
python -m unittest test_integration.py
```

## Notes

- The database file (`database.db`) and environment file (`.env`) are ignored by git.
- Make sure the server is running before starting the client.
- You can adjust the number of cars generated in `populate.py` by changing `NUM_CARS_TO_GENERATE