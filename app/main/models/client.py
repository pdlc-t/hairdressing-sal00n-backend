from app.extensions import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    second_name = db.Column(db.String(40), nullable=False)
    login = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "second_name": self.second_name
        }