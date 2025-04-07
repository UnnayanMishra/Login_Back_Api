from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)  # ✅ Add this to allow CORS

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))  # Fallback to 3306 if not set
}

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()

    if 'username' not in data:
        return jsonify({'message': 'Username is required'}), 400

    username = data['username']

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT link FROM user_credentials WHERE user_name = %s", (username,))
        result = cursor.fetchone()

        if result:
            return jsonify({'exists': True, 'link': result['link']})
        else:
            return jsonify({'exists': False})

    except mysql.connector.Error as err:
        return jsonify({'message': str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
