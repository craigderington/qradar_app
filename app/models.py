from app import db
from datetime import datetime, timedelta
from sqlalchemy.orm import validates


class Message(db.Model):
    """
    Message Class
    :return message
    """
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(64), nullable=False)
    message_text = db.Column(db.String(255), nullable=False)
    message_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    sender = db.Column(db.String(64), nullable=False)
    sent_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    message_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        if self.id and self.message_type:
            return "{} {}".format(self.id, self.message_type)
