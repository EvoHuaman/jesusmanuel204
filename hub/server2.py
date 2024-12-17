# server2.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

SERVER_1_URL = 'http://127.0.0.1:5000/users'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'email': request.form['email']
    }
    response = requests.post(SERVER_1_URL, json=data)
    return response.json()

@app.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    response = requests.get(f"{SERVER_1_URL}/{user_id}")
    return response.json()

@app.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email')
    }
    response = requests.put(f"{SERVER_1_URL}/{user_id}", json=data)
    return response.json()

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    response = requests.delete(f"{SERVER_1_URL}/{user_id}")
    return response.json()

if __name__ == '__main__':
    app.run(port=5001)
