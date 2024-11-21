import mysql.connector

def test_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123.",
            database="adminerp_garden"
        )
        print("Conexión exitosa")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

test_connection()
