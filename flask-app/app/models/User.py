from app import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Text)
    active_book_id = db.Column(db.Integer)
    book_section = db.Column(db.Integer)

    def __init__(self, phone_number, active_book_id, book_section):
        self.phone_number = phone_number
        self.active_book_id = active_book_id
        self.book_section = active_book_section
