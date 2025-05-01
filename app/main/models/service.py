from app.extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serviceName = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time = db.Column(db.Integer, nullable=False)          # in minutes
    availability = db.Column(db.String(100))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "serviceName": self.serviceName,
            "price": self.price,
            "time": self.time,
            "availability": self.availability,
            "description": self.description
        }
