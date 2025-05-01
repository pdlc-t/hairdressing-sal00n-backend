from app.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer)
    producer = db.Column(db.String(100))
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "productName": self.productName,
            "price": self.price,
            "amount": self.amount,
            "producer": self.producer,
            "description": self.description
        }
