from flask import Flask, render_template
from mysql.connector import cursor
import mysql.connector

app = Flask(__name__)
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Uma@2704",
        database="saferteck"
    )
        
    def index():
        query_join = """
            SELECT locations.location_id, locations.street_address, locations.city, locations.state_province, countries.country_name
            FROM locations
            JOIN countries ON locations.country_id = countries.country_id
            WHERE countries.country_name = 'Canada'
            """

        cursor = db_connection.cursor()
        cursor.execute(query_join)

        results_join = cursor.fetchall()
        cursor.close()
        query_without_join = """
                    SELECT location_id, street_address, city, state_province, 'Canada' AS country_name
                    FROM locations
                    WHERE country_id = (
                        SELECT country_id FROM countries WHERE country_name = 'Canada'
                    )
                    """
        cursor = db_connection.cursor()
        cursor.execute(query_without_join)
        results_without_join = cursor.fetchall()
        cursor.close()

        return render_template('index.html', results_join=results_join, results_without_join=results_without_join)

    @app.route('/')
    def home():
        return index()


    if __name__ == '__main__':
        app.run(debug=True)

except mysql.connector.Error as e:
    print("Error:", e)

   
