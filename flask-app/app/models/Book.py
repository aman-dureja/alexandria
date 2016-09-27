from app import db

class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    language = db.Column(db.Text)
    difficulty_level = db.Column(db.Text)
    times_subscribed = db.Column(db.Integer)
    # snippets = db.relationship('Snippet', backref='book', lazy='select')
    # lazy defines when SQLAlchemy will load data from the database
    # options are: `select` - standard select statement,
    #              `joined` - load relationship in same query as parent via JOIN,
    #              `subquery` - like `joined` but will use subquery,
    #              `dynamic` - useful for many items; returns query object that can be further refined

    def __init__(self, title, author, language, difficulty_level, times_subscribed):
        self.title = title
        self.author = author
        self.language = language
        self.difficulty_level = difficulty_level
        self.times_subscribed = times_subscribed
