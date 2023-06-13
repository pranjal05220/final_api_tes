from aiprofile_api.utils.dumpcsvdata import PostgreSQLConnector
import psycopg2
from flask import Flask, request, jsonify, Blueprint


app = Flask(__name__)

postgreetest = Blueprint("postgreetest", __name__, url_prefix="/postgreetest")


@postgreetest.route('/', methods=["OPTIONS", "GET"])
def home():
    return "Home of postgresql_database ", 200


@postgreetest.route('/data', methods=["OPTIONS", "POST"])
def upload_data():
    try:
        connection = PostgreSQLConnector()
        if connection is None:
            return jsonify({'error': 'Failed to connect to the database'})

        csv_file_path = r"C:\Users\hp\PycharmProjects\aiprofile\data\data.csv"
        connection.import_csv_data(csv_file_path)

        return "Data dumped successfully", 200

    except psycopg2.Error as e:
        print("Error fetching data from the database:", e)
        return jsonify({'error': 'Failed to fetch data from the database'})

