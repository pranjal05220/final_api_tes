import csv
import psycopg2

# PostgreSQL connection details
db_host = 'localhost'
db_port = '5432'
db_name = 'api_database'
db_user = 'postgres'
db_password = 'example'


class PostgreSQLConnector:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS pranjal_data (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                voltage INTEGER,
                current INTEGER
            )
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_row(self, row):
        self.cur.execute(
            "INSERT INTO pranjal_data (timestamp, voltage, current) VALUES (%s, %s, %s)",
            (row[0].strip(), int(row[1]), int(row[2]))
        )

    def process_csv_data(self, csv_data):
        for row in csv_data:
            self.insert_row(row)

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def import_csv_data(self, csv_file_path):
        with open(csv_file_path, mode="r") as file:
            csv_data = csv.reader(file)
            self.process_csv_data(csv_data)
            self.conn.commit()


if __name__ == "__main__":
    csv_file_path = r"C:\Users\hp\PycharmProjects\aiprofile\data\data.csv"

    try:
        connection = PostgreSQLConnector(db_host, db_port, db_name, db_user, db_password)
        connection.import_csv_data(csv_file_path)
        connection.close_connection()
        print("Data imported successfully!")
    except psycopg2.Error as e:
        print("Error importing data:", e)
