import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from modules import savepassword, key, generate, passwordcheck
import getpass

def secure_getpass(prompt):
    return getpass.getpass(prompt)

key_file_path = os.path.join("D:/", '.env')
user_password = secure_getpass("Enter a password to protect the key: ")
pkey = key.keys(key_file_path, user_password)
if pkey == "Incorrect password":
    print("Incorrect password")
    exit()

app = Flask(__name__)
CORS(app, resources={r"/get_password": {"origins": "http://localhost:port"}})  # Limit CORS

@app.route('/get_password', methods=['GET'])
def get_password():
    try:
        site = request.args.get('site')
        db_path = "D:/passwords.db"
        key_file_path = os.path.join("D:/", '.env')
        
        if not os.path.exists(db_path):
            return jsonify({'error': 'Database file not found'}), 404  # Return 404 for not found

        if not os.path.exists(key_file_path):  # Check if key file exists
            return jsonify({'error': 'Key file not found'}), 404

        site, user, password = savepassword.decrypt_password_from_db(site, db_path, pkey)
        return jsonify({'site': site, 'user': user, 'password': password})
    except:
        return jsonify({'error': 'Site not found'}), 404

@app.route('/save_password', methods=['POST'])
def save_password():
    try:
        site = request.json.get('site')
        user = request.json.get('user')
        password = request.json.get('password')

        db_path = "D:/passwords.db"
        key_file_path = os.path.join("D:/", '.env')

        if not os.path.exists(db_path):
            return jsonify({'error': 'Database file not found'}), 404  # Return 404 for not found

        if not os.path.exists(key_file_path):  # Check if key file exists
            return jsonify({'error': 'Key file not found'}), 404
        if password == "g":
            password = generate.main()
        elif passwordcheck.password_strength(password) != 'Strong password':
            return jsonify({'error': 'Password does not meet all requirements'}), 500

        savepassword.save_password_to_db(site, user, password, db_path, pkey)
        return jsonify({'message': 'Password saved successfully'})
    except FileNotFoundError as e:  # Handle specific exception
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == "__main__":
    app.run(port=5000)