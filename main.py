from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/", methods=["GET"])
def index():
    return "<h1>GUD</h1>"


@app.route("/api/v1/resources/books/all", methods=["GET"])
def api_all():
    conn = sqlite3.connect("DB/books.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute("select * from books;").fetchall()
    return jsonify(all_books)


@app.route("/api/v1/resources/books", methods=["GET"])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get("id")
    published = query_parameters.get("published")
    author = query_parameters.get("author")
    query = "select * from books where"
    to_filter = []

    if id:
        query += " id=? and"
        to_filter.append(id)
    if published:
        query += " published=? and"
        to_filter.append(published)
    if author:
        query += " author=? and"
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)
    query = query[:-4] + ";"
    conn = sqlite3.connect("DB/books.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute(query, to_filter).fetchall()
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run()
