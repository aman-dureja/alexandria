from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import urllib2
import json
from random import randint
import MySQLdb

sys.path.append('./app/modules')
sys.path.append('./app/models')

from User import User
from Book import Book
from Snippet import Snippet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hackathonmans@104.155.149.246/alexandria_v3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Command():
    read = "read"
    get_help = "help"
    dictionary = "dict"
    best = "best"
    next_snippet = "next"
    prev_snippet = "previous"
    stop = "stop"

# HELPERS

def get_user(number):
    return User.query.filter_by(phone_number = number).first()

# MODULES

def read_module(current_user, param_after_command):

    difficulties = ['easy', 'medium', 'hard']

    if param_after_command in difficulties or param_after_command == None:

        if param_after_command == None:

        	total_num_books = db.session.query(Book).count()
        	random_book_id = randint(1, total_num_books)
        	current_user.active_book_id = random_book_id

        else:
        	random_book_id = random.choice(Book.query.filter_by(difficulty_level = param_after_command).all()).book_id
        	current_user.active_book_id = random_book_id

        current_user.book_section = 1
        db.session.commit()
        snippet_to_send = Book.query.filter_by(book_id = random_book_id).first().content

        return snippet_to_send

    # TODO: Add logic to handle variance in book title name, i.e. capitalization
    book_title = param_after_command

    if Book.query.filter_by(title = book_title).count() == 0:
        # Book not found, define expected behavior or return error message here
        return "Book not found in database"
    else:
        current_user.active_book_id = Book.query.filter_by(title = book_title).first().book_id
        current_user.book_section = 1
        db.session.commit()

        # TODO: return message to user saying book has been subscribed to

        snippet_to_send = Snippet.query.filter_by(book_id = current_user.active_book_id).filter_by(book_section = current_user.book_section).first()
        # TODO: send snippet to user via Twilio

        # for now, simply return snippet
        return snippet_to_send

def best_module(difficulty=None):

    best_books = None

    # Get top 10 books
    if difficulty:
        best_books = Book.query.filter_by(difficulty_level = difficulty).order_by(Book.times_subscribed.desc()).limit(10)
    else:
        best_books = Book.query.order_by(Book.times_subscribed.desc()).limit(10)

    result = ""

    for book in best_books:
        result += book.title + "\n"

    return result

def dict_module(word):
    url = "http://api.pearson.com/v2/dictionaries/entries?headword="
    url += word

    request = urllib2.Request(url)
    response = urllib2.urlopen(url)
    result = json.loads(response.read.decode(encoding="utf-8"))

    return result["results"][0]["senses"][0]["definition"]


def stop_module(current_user):
    if current_user.active_book_id == 0:
        return "User not subscribed to a book!"
    else:
        # current_user.active_book_id = 0
        # current_user.book_section = 0
        db.session.query(User).filter_by(phone_number = current_user.phone_number).update({"active_book_id":0, "book_section":0})
        db.session.commit()
        return "Successfully unsubscribed from book"

def next_snippet_module(current_user):
    mysqldb = MySQLdb.connect("104.155.149.246","root","hackathonmans","alexandria_v3" )
    cursor = mysqldb.cursor()

    if current_user.active_book_id == 0:
       return "User not subscribed to a book"
    else:
        # TODO: Check that there exists a next snippet in the db to return
        # if current_user.book_section ==
        #next_section = current_user.book_section + 1
        #snippet_content = db.session.query(Snippet).filter_by(book_id = current_user.active_book_id).filter_by(section = next_section).first().content
        #db.session.query(User).filter_by(phone_number = current_user.phone_number).update({"book_section": next_section})
        #db.session.flush()

        try:
            cursor.execute ("""UPDATE users
                               SET book_section=%s
                               WHERE phone_number=%s""", (current_user.book_section+1, current_user.phone_number))
            mysqldb.commit()
        except:
            mysqldb.rollback()

        mysqldb.close()

        return "Test"

def prev_snippet_module(current_user):
    mysqldb = MySQLdb.connect("104.155.149.246","root","hackathonmans","alexandria_v3" )
    cursor = mysqldb.cursor()

    if current_user.active_book_id == 0:
        return "User not subscribed to a book"
    else:
        if current_user.book_section > 1:
            cursor.execute ("""UPDATE users
                               SET book_section=%s
                               WHERE phone_number=%s""", (current_user.book_section-1, current_user.phone_number))
            mysqldb.commit()
            mysqldb.close()
            return "tent"
        else:
            return "You are on the first page of the book!"

def help_module():
    return """help -- Get list of available commands
    read -- Subscribe to a random book
    read <BOOK-NAME> -- Subscribe to a book of your choice
    read <DIFFICULTY> -- Subscribe to a random book of a given DIFFICULTY
    best -- See list of top 10 read books
    next -- Get the next snippet of the book
    previous -- Get the previous snippet of the book
    stop -- Stop your subscription to the current book
    """

@app.route("/next")
def test2():
    current_user = get_user("123-456-7890")
    print next_snippet_module(current_user)
    current_user2 = get_user("911-911-1234")
    print next_snippet_module(current_user2)
    return "Yay"

@app.route("/prev")
def test3():
    current_user = get_user("123-456-7890")
    print prev_snippet_module(current_user)
    current_user2 = get_user("911-911-1234")
    print prev_snippet_module(current_user2)
    return "Yay"

@app.route("/read")
def test4():
    current_user = get_user("123-456-7890")
    print read_module(current_user,"You Should Use Rails")
    return 'Yay'

@app.route("/", methods=['GET', 'POST'])
def parse_command():

    # Get body of text message from Twilio
    data = request.form.get('Body')
    phone_num = request.form.get('From')
    splitData = data.split(" ")
    # User object
    current_user = None

    # Array of all users who use this
    user = User.query.filter_by(phone_number = phone_num)
    if len(user) == 0:
        # Assume 0 for no book, no section
        new_user = User(phone_num, 0, 0)
        db.session.add(new_user)
        db.session.commit()
        current_user = new_user
        #send text message to user here upon success
    else:
        current_user = user[0]

    # Check if user exists in db, if not =>

    user_command = splitData[0]
    additional_data = None

    if len(splitData) >= 2:
        additional_data = splitData[1]

    if user_command == Command.read:
        text_to_send = read_module(current_user, additional_data)

    elif user_command == Command.dictionary:
        text_to_send = dict_module(additional_data)

    elif user_command == Command.get_help:
        text_to_send = help_module()

    elif user_command == Command.best:
        text_to_send = best_module(additional_data)

    elif user_command == Command.next_snippet:
        text_to_send = next_snippet_module(current_user)

    elif user_command == Command.prev_snippet:
        text_to_send = prev_snippet_module(current_user)

    elif user_command == Command.stop:
        text_to_send = stop_module(current_user)


if __name__ == "__main__":
    app.run()
