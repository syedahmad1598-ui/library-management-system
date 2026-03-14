from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        issued_to TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    cur.execute("SELECT * FROM members")
    members = cur.fetchall()

    total_books = len(books)
    total_members = len(members)

    conn.close()

    return render_template(
        "index.html",
        books=books,
        members=members,
        total_books=total_books,
        total_members=total_members
    )


@app.route("/add_book", methods=["POST"])
def add_book():

    title = request.form["title"]
    author = request.form["author"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO books (title, author) VALUES (?,?)",
        (title, author)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/add_member", methods=["POST"])
def add_member():

    name = request.form["name"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO members (name) VALUES (?)",
        (name,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/issue/<int:id>")
def issue_book(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE books SET issued_to='Issued' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/return/<int:id>")
def return_book(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE books SET issued_to=NULL WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )

    books = cur.fetchall()

    cur.execute("SELECT * FROM members")
    members = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        books=books,
        members=members,
        total_books=len(books),
        total_members=len(members)
    )


if __name__ == "__main__":
    app.run(debug=True)