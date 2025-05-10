from app.extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    hairdresser_id = db.Column(db.Integer, db.ForeignKey('hairdressers.id'), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'hairdresser_id': self.hairdresser_id,
            'author': self.author,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }
