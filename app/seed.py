# seed.py
import json
from app.extensions import db
from app.main.models.hairdresser import Hairdresser
from app.main.models.comment import Comment
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

# Comments for each hairdresser, parallel by index
COMMENTS_JSON = [
    [  # for Anna
        {"author": "Jan Kowalski", "content": "Świetne cięcie, polecam!"},
        {"author": "Anna Nowak",   "content": "Bardzo miła obsługa."}
    ],
    [  # for Amelia
        {"author": "Marcin Wiśniewski", "content": "Profesjonalnie i szybko."}
    ],
    [  # for Ewa
        # no comments
    ],
    [  # for Tomasz
        {"author": "Kasia Lewandowska", "content": "Polecam, świetne farbowanie!"},
        {"author": "Piotr Wójcik",      "content": "Mogłoby być nieco tańsze."}
    ],
    [  # for Katarzyna
        {"author": "Magda Zielińska", "content": "Super manicure."}
    ]
]

SERVICES_JSON = [
    {"serviceName": "Strzyżenie Męskie",      "price": 50,  "time": 30, "availability": "dostępne", "description": "Przykładowy opis usługi strzyżenia męskiego."},
    {"serviceName": "Strzyżenie Damskie",     "price": 70,  "time": 45, "availability": "dostępne", "description": "Przykładowy opis usługi strzyżenia damskiego."},
    {"serviceName": "Manicure",               "price": 60,  "time": 40, "availability": "dostępne", "description": "Przykładowy opis usługi manicure."},
    {"serviceName": "Farbowanie włosów długich", "price":120,"time": 90, "availability": "dostępne", "description": "Przykładowy opis usługi farbowania włosów długich."}
]

PRODUCTS_JSON = [
    {"productName": "Szampon DX2", "price": 10, "amount": 30, "producer": "DX2.sp.zoo", "description": "Przykładowy opis szamponu."},
    {"productName": "Odżywka ABC", "price": 15, "amount": 20, "producer": "ABC Ltd.",    "description": "Przykładowy opis odżywki."},
    {"productName": "Maska XYZ",   "price": 25, "amount": 10, "producer": "XYZ Co.",      "description": "Przykładowy opis maski."}
]

def seed_database():
    """Zasiej przykładowe dane wraz z komentarzami, ale tylko jeśli baza jest pusta."""
    # Czy już są jakiekolwiek fryzjerzy?
    if Hairdresser.query.first():
        return

    # 1) Zasiewanie fryzjerów i ich komentarzy
    for idx, entry in enumerate(HAIRDRESSERS_JSON):
        hd = Hairdresser(
            firstName  = entry['firstName'],
            lastName   = entry['lastName'],
            specialties= json.dumps(entry['specialties']),
            rating     = entry['rating']
        )
        db.session.add(hd)
        db.session.flush()  # potrzebne, aby hd.id było dostępne od razu

        # dodaj komentarze
        for c in COMMENTS_JSON[idx]:
            comment = Comment(
                hairdresser_id = hd.id,
                author         = c.get('author'),
                content        = c.get('content')
            )
            db.session.add(comment)

    # 2) Zasiewanie usług
    for entry in SERVICES_JSON:
        svc = Service(
            serviceName = entry['serviceName'],
            price       = entry['price'],
            time        = entry['time'],
            availability= entry['availability'],
            description = entry['description']
        )
        db.session.add(svc)

    # 3) Zasiewanie produktów
    for entry in PRODUCTS_JSON:
        prod = Product(
            productName = entry['productName'],
            price       = entry['price'],
            amount      = entry['amount'],
            producer    = entry['producer'],
            description = entry['description']
        )
        db.session.add(prod)

    # 4) Zatwierdzenie wszystkich zmian
    db.session.commit()
    print("✅ Baza została zasilona przykładowymi fryzjerami z komentarzami oraz usługami i produktami.")
