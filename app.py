from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import logging

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Host: sql12.freesqldatabase.com
# Database name: sql12773179
# Database user: sql12773179
# Database password: W8lWH92EGm
# Port number: 3306


# Database configuration from environment variables
db_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773179',
    'password': 'W8lWH92EGm',
    'database': 'sql12773179',
    'port': 3306  # Default MySQL port
}


@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()

    if not data or 'username' not in data:
        return jsonify({'message': 'Username is required'}), 400

    username = data['username'].strip()

    if not username:
        return jsonify({'message': 'Invalid username'}), 400

    connection = None
    cursor = None

    try:
        # Connect to database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch user
        query = "SELECT link FROM user_credentials WHERE user_name = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            return jsonify({'exists': True, 'link': result['link']})
        else:
            return jsonify({'exists': False})

    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        return jsonify({'message': 'Database error: ' + str(err)}), 500

    except Exception as e:
        logging.exception("Unexpected error occurred")
        return jsonify({'message': 'Internal server error'}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    # Use port 10000 as specified
    app.run(host='0.0.0.0', port=10000)
