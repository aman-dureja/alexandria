from app import db

class Snippet(db.Model):

	__tablename__ = 'snippets'

	id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer)
	section = db.Column(db.Integer)
	content = db.Column(db.Text)

	def __init__(self, book_id, section, content):
		self.book_id = book_id
		self.section = section
		self.content = content
