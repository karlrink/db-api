
# python3

__version__='0.0.1.dev.20210427-1'

from app import app
from flask import request
from flask import jsonify
from werkzeug.exceptions import HTTPException
from db import mysql
import cryptography
from functools import wraps


@app.route("/", methods=['GET'])
def root():
    return jsonify(status=200, message="OK", version=__version__), 200


@app.route("/api", methods=['GET'])
def show_databases():
    SQL = 'SHOW DATABASES'
    rows = fetchall(SQL)
    return jsonify(rows), 200


@app.route("/api/<db>", methods=['GET'])
def show_tables(db=None):
    assert db == request.view_args['db']
    SQL = 'SHOW TABLES FROM ' + str(db)
    rows = fetchall(SQL)
    return jsonify(rows), 200


@app.route("/api/<db>/<table>", methods=['GET'])
def get_api(db=None, table=None):

    assert db == request.view_args['db']
    assert table == request.view_args['table']

    fields = request.args.get("fields", None)
    limit  = request.args.get("limit", None)

    if not request.query_string:
        SQL = 'SHOW FIELDS FROM ' + str(db) +'.'+ str(table)
        rows = fetchall(SQL)
        return jsonify(rows), 200

    if not fields:
        fields = '*'

    SQL = 'SELECT '+ str(fields) +' FROM '+ str(db) +'.'+ str(table) 

    if limit:
        SQL += ' LIMIT ' + str(limit)

    rows = fetchall(SQL)
    return jsonify(rows), 200


@app.errorhandler(404)
def not_found(error=None):
    message = { 'status': 404, 'errorType': 'Not Found: ' + request.url }
    return jsonify(message), 404


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    res = {'status': 500, 'errorType': 'Internal Server Error'}
    res['errorMessage'] = str(e)
    return jsonify(res), 500


def Auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app.config['MYSQL_DATABASE_USER'] = request.authorization.username
        app.config['MYSQL_DATABASE_PASSWORD'] = request.authorization.password
        app.config['MYSQL_DATABASE_HOST'] = request.headers.get('X-Host', '127.0.0.1')
        app.config['MYSQL_DATABASE_PORT'] = int(request.headers.get('X-Port', '3306'))
        return f(*args, **kwargs)
    return decorated


@Auth
def fetchall(sql):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@Auth
def fetchone(sql):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row




if __name__ == "__main__":
    app.run(port=8980, debug=False)


