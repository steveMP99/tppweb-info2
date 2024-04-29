from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from models import auth


app = auth.app


if __name__ == '__main__':
    app.run(debug=True)