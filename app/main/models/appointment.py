# app/main/models/appointment.py

from app.extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    hairdresser_id = db.Column(db.Integer, db.ForeignKey('hairdressers.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    time_slot = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)   # <-- nowa kolumna

    service = db.relationship('Service')
    client = db.relationship('Client')
    hairdresser = db.relationship('Hairdresser')

    def to_dict(self):
        return {
            "id": self.id,
            "client": f"{self.client.first_name} {self.client.second_name}",
            "service_name": self.service.serviceName,
            "price": self.service.price,
            "hairdresser": {
                "id": self.hairdresser.id,
                "firstName": self.hairdresser.firstName,
                "lastName": self.hairdresser.lastName
            },
            "date": self.date.isoformat(),
            "time_slot": self.time_slot,
            "rating": self.rating   # <-- uwzględnij w zwracanym obiekcie
        }
