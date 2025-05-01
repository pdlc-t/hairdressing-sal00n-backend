from app.extensions import db

class Hairdresser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    specialties = db.Column(db.String, nullable=False)  # store JSON list as text
    rating = db.Column(db.Integer)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "specialties": json.loads(self.specialties),
            "rating": self.rating
        }
