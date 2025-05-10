from app.extensions import db
import json

class Hairdresser(db.Model):
    __tablename__ = 'hairdressers'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    specialties = db.Column(db.String, nullable=False)  # stored as JSON text
    rating = db.Column(db.Integer)

    # relational link to comments
    comments = db.relationship(
        'Comment',
        backref='hairdresser',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'specialties': json.loads(self.specialties),
            'rating': self.rating,
            'comments': [c.to_dict() for c in self.comments]
        }
