from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import bookDB

app = Flask(__name__)
db = bookDB.bookDB("mylib")

@app.route('/')
def hello_world():
    count = len(db.listAllBooks())
    return render_template("mainPage.html", count_books=count)

@app.route('/addBooksForm')
def add_Book_Form():
    return render_template("addBookTemplate.html")

@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
    if request.method == "GET":
        db.addBook(request.form["Author"], request.form["Title"], request.form["Year"])
        return str(request.args)
    else:
        db.addBook(request.form["Author"], request.form["Title"], request.form["Year"])
        return str(request.form)
    return render_template("addBookTemplate.html")


@app.route('/API/book/<int:id>')
def show_Book(id):
    return jsonify(str(db.showBook(id)))

@app.route('/API/books')
def list_All_Books():
    raw_books = db.listAllBooks()
    books = []
    for i in range(len(raw_books)):
        books.append(str(raw_books[i]))
    return jsonify(books)

@app.route('/API/authorbooks/<author>')
def list_Books_Author_Form(author):
    raw_books = db.listBooksAuthor(author)
    books = []
    for i in range(len(raw_books)):
        books.append(str(raw_books[i]))
    return jsonify(books)

@app.route('/API/yearbooks/<int:year>')
def list_Books_Year_Form(year):
    raw_books = db.listBooksYear(year)
    books = []
    for i in range(len(raw_books)):
        books.append(str(raw_books[i]))
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug = True)