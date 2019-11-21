from flask import Flask
from flask import render_template
from flask import request
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

@app.route('/showBookForm')
def show_Book_Form():
    return render_template("showBookTemplate.html")

@app.route('/showBook')
def show_Book():
    try:
        book = db.showBook(int(request.args["id"]))
    except Exception:
        book = None

    if book == None:
        return "Book does not exist"
    else:
        return str(book)

@app.route('/listAllBooks')
def list_All_Books():
    return render_template("listAllBooks.html", keys = db.listAllBooks())

@app.route('/listBooksAuthorForm')
def list_Books_Author_Form():
    return render_template("listBooksAuthorTemplate.html")

@app.route('/listBooksAuthor')
def list_Books_Author():
    try:
        book_list = db.listBooksAuthor(request.args["author"])
    except Exception:
        book_list = None

    if book_list == None:
        book_list.append("No books found")
    
    return render_template("listBooksAuthor.html", keys = book_list)

@app.route('/listBooksYearForm')
def list_Books_Year_Form():
    return render_template("listBooksYearTemplate.html")

@app.route('/listBooksYear')
def list_Books_Year():
    try:
        book_list = db.listBooksYear(int(request.args["year"]))
    except Exception:
        book_list = []

    if book_list == None:
        book_list.append("No books found ")
    
    return render_template("listBooksYear.html", keys = book_list)


if __name__ == '__main__':
    app.run(debug = True)