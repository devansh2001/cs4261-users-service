from logging import debug
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/health-check')
def health_check():
    return {'status': 'OK', 'code': '200'}

@app.route('/create-user')
def create_user():
    return {'status': 201}

@app.route('/get-user/<user_id>')
def get_user(user_id):
    return {'status': 200}

@app.route('/delete-user/<user_id>')
def delete_user(user_id):
    return {'status': 200}

@app.route('/authenticate')
def authenticate():
    return {'status': 200}

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)