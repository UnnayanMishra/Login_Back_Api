from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database config
db_config = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12771518',
    'password': 'RARPZ8uhWN',
    'database': 'sql12771518',
    'port': 3306
}

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()

    # Validate input
    if 'username' not in data:
        return jsonify({'error': 'Username is required'}), 400

    username = data['username']

    try:
        # Connect to database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query for user
        cursor.execute("SELECT link FROM user_credentials WHERE user_name = %s", (username,))
        result = cursor.fetchone()

        if result:
            return jsonify({'exists': True, 'link': result['link']})
        else:
            return jsonify({'exists': False})

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

