# server1.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user database
users = {}

# Add User
@app.route('/users', methods=['POST'])
def add_user():
    user_id = request.json.get('id')
    name = request.json.get('name')
    email = request.json.get('email')
    if user_id in users:
        return jsonify({"error": "User already exists"}), 400
    users[user_id] = {'name': name, 'email': email}
    return jsonify({"message": "User added successfully"}), 201

# Retrieve User
@app.route('/users/<user_id>', methods=['GET'])
def retrieve_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# Update User
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    name = request.json.get('name')
    email = request.json.get('email')
    if name:
        users[user_id]['name'] = name
    if email:
        users[user_id]['email'] = email
    return jsonify({"message": "User updated successfully"}), 200

# Delete User
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)
