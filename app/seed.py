# seed.py
import json
from app.extensions import db
from app.main.models.hairdresser import Hairdresser
from app.main.models.service import Service
from app.main.models.product import Product

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

    db.session.commit()
    print("✅ Baza została zasilona przykładowymi danymi.")