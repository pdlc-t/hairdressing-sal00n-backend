# seed.py
import json
from datetime import datetime
from app.extensions import db
from app.main.models.hairdresser import Hairdresser
from app.main.models.service import Service
from app.main.models.product import Product
from app.main.models.client import Client
from app.main.models.appointment import Appointment

# Sample data
HAIRDRESSERS_JSON = [
  {
    "firstName": "Anna",
    "lastName": "Kowalska",
    "specialties": ["strzyżenie męskie", "strzyżenie damskie", "farbowanie"],
    "rating": 5
  },
  {
    "firstName": "Amelia",
    "lastName": "Brogowicz",
    "specialties": ["strzyżenie męskie", "manicure"],
    "rating": 5
  },
  {
    "firstName": "Ewa",
    "lastName": "Wiśniewska",
    "specialties": ["strzyżenie damskie", "farbowanie", "manicure"],
    "rating": 3
  },
  {
    "firstName": "Tomasz",
    "lastName": "Zieliński",
    "specialties": ["strzyżenie męskie", "strzyżenie damskie"],
    "rating": 4
  },
  {
    "firstName": "Katarzyna",
    "lastName": "Lewandowska",
    "specialties": ["farbowanie", "manicure"],
    "rating": 5
  }
]

SERVICES_JSON = [
  {"serviceName": "Strzyżenie Męskie", "price": 50, "time": 30, "availability": "dostępne", "description": "Przykładowy opis usługi strzyżenia męskiego."},
  {"serviceName": "Strzyżenie Damskie", "price": 70, "time": 45, "availability": "dostępne", "description": "Przykładowy opis usługi strzyżenia damskiego."},
  {"serviceName": "Manicure", "price": 60, "time": 40, "availability": "dostępne", "description": "Przykładowy opis usługi manicure."},
  {"serviceName": "Farbowanie włosów długich", "price": 120, "time": 90, "availability": "dostępne", "description": "Przykładowy opis usługi farbowania włosów długich."}
]

PRODUCTS_JSON = [
  {"productName": "Szampon DX2", "price": 10, "amount": 30, "producer": "DX2.sp.zoo", "description": "Przykładowy opis szamponu."},
  {"productName": "Odżywka ABC", "price": 15, "amount": 20, "producer": "ABC Ltd.", "description": "Przykładowy opis odżywki."},
  {"productName": "Maska XYZ", "price": 25, "amount": 10, "producer": "XYZ Co.", "description": "Przykładowy opis maski."}
]

CLIENTS_JSON = [
    {"first_name": "fufuk", "second_name": "gnufuk", "login": "login1", "password_hash": "passwd1"},
    {"first_name": "Liora", "second_name": "Skydancer", "login": "login2", "password_hash": "passwd2"},
    {"first_name": "Taren", "second_name": "Stoneveil", "login": "login3", "password_hash": "passwd3"},
    {"first_name": "Elira", "second_name": "Moondust", "login": "login4", "password_hash": "passwd4"},
    {"first_name": "Caelum", "second_name": "Nightbloom", "login": "login5", "password_hash": "passwd5"},
    {"first_name": "Sylas", "second_name": "Ashwhisper", "login": "login6", "password_hash": "passwd6"}
]

APPOINTMENTS_JSON = [
    {"client_id": 3, "service_id": 2, "date": "2025-05-10T10:00:00+00:00", "time_slot": 1},
    {"client_id": 1, "service_id": 1, "date": "2025-05-10T10:00:00+00:00", "time_slot": 2},
    {"client_id": 2, "service_id": 3, "date": "2025-05-10T10:00:00+00:00", "time_slot": 3},
    {"client_id": 4, "service_id": 2, "date": "2025-05-10T10:00:00+00:00", "time_slot": 4},
    {"client_id": 5, "service_id": 1, "date": "2025-05-10T10:00:00+00:00", "time_slot": 5},
    {"client_id": 6, "service_id": 4, "date": "2025-04-30T10:00:00+00:00", "time_slot": 1},
    {"client_id": 2, "service_id": 2, "date": "2025-04-30T10:00:00+00:00", "time_slot": 2},
    {"client_id": 1, "service_id": 4, "date": "2025-04-30T10:00:00+00:00", "time_slot": 3},
    {"client_id": 3, "service_id": 3, "date": "2025-04-30T10:00:00+00:00", "time_slot": 4},
    {"client_id": 4, "service_id": 1, "date": "2025-05-12T10:00:00+00:00", "time_slot": 1},
    {"client_id": 6, "service_id": 2, "date": "2025-05-12T10:00:00+00:00", "time_slot": 2}
]


def seed_database():
    """Zasiej przykładowe dane, ale tylko jeśli tabela Hairdresser jest pusta."""
    if Hairdresser.query.first():
        return

    # fryzjerzy
    for entry in HAIRDRESSERS_JSON:
        hd = Hairdresser(
            firstName=entry['firstName'],
            lastName=entry['lastName'],
            specialties=json.dumps(entry['specialties']),
            rating=entry['rating']
        )
        db.session.add(hd)

    # usługi
    for entry in SERVICES_JSON:
        svc = Service(
            serviceName   = entry['serviceName'],
            price         = entry['price'],
            time          = entry['time'],
            availability  = entry['availability'],
            description   = entry['description']
        )
        db.session.add(svc)

    # produkty
    for entry in PRODUCTS_JSON:
        prod = Product(
            productName = entry['productName'],
            price       = entry['price'],
            amount      = entry['amount'],
            producer    = entry['producer'],
            description = entry['description']
        )
        db.session.add(prod)

    for entry in CLIENTS_JSON:
        client = Client(
            first_name = entry['first_name'],
            second_name = entry['second_name'],
            login = entry['login'],
            password_hash = entry['password_hash']
        )
        db.session.add(client)

    db.session.commit()

    for entry in APPOINTMENTS_JSON:
        appointment = Appointment(
            client_id = entry['client_id'],
            service_id = entry['service_id'],
            date = datetime.fromisoformat(entry['date']),
            time_slot = entry['time_slot']
        )
        db.session.add(appointment)

    db.session.commit()
    print("✅ Baza została zasilona przykładowymi danymi.")