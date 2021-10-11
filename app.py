from logging import debug
from flask import Flask, request
import os
import psycopg2
import uuid
import json
from flask_cors import CORS

app = Flask(__name__)
# https://stackoverflow.com/a/64657739
CORS(app)
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# https://stackoverflow.com/a/43634941
conn.autocommit = True

cursor = conn.cursor()
try:

    cursor.execute('''
        DROP TABLE IF EXISTS users;
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id varchar(64) PRIMARY KEY,
        fname varchar(256),
        lname varchar(256),
        phone_number varchar(15),
        venmo_id varchar(128),
        user_location varchar(64),
        email varchar(256),
        password varchar(64),
        user_type varchar(32)
    );
    ''')
except psycopg2.Error:
    print('Error occurred while creating table')
    
    # cursor.execute('INSERT INTO users (fname, lname) VALUES (%s, %s)', ['Devansh', 'Ponda'])
    # cursor.execute('INSERT INTO users (fname, lname) VALUES (%s, %s)', ['Tusheet', 'Goli'])
    
    # cursor.execute('SELECT * FROM users')
    # print(cursor.fetchall())
    # res = cursor.fetchall()
    # print(res)

    # Check if table exists


@app.route('/health-check')
def health_check():
    return {'status': 'OK', 'code': '200'}

@app.route('/create-user', methods=['POST'])
def create_user():
    # https://stackoverflow.com/a/67461897
    data = request.get_json()
    fname = data['fname']
    lname = data['lname']
    phone_number = data['phone_number']
    venmo_id = data['venmo_id']
    user_location = data['user_location']
    email = data['email']
    password = data['password']
    user_type = data['user_type']
    user_id = str(uuid.uuid4())
    query = '''
        INSERT INTO users (user_id, fname, lname, phone_number, venmo_id, user_location, email, password, user_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(query, [user_id, fname, lname, phone_number, venmo_id, user_location, email, password, user_type])
    
    return {'status': 201, 'user_id': user_id}

@app.route('/get-user/<user_id>')
def get_user(user_id):
    query = '''
        SELECT * FROM users where users.user_id=%s
    '''

    cursor.execute(query, [str(user_id)])
    res = cursor.fetchall()
    if (len(res) == 0):
        return {'status': 200, 'user': None}

    user = {
        'user_id': res[0][0],
        'fname': res[0][1],
        'lname': res[0][2],
        'email': res[0][6],
        'venmo_id': res[0][4],
        'phone_number': res[0][3],
        'user_type': res[0][8],
        'user_location': res[0][5]
    }
    return {'status': 200, 'user': user}

@app.route('/delete-user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = '''
        DELETE FROM users WHERE users.user_id=%s
    '''
    cursor.execute(query, [str(user_id)])
    return {'status': 200}

@app.route('/authenticate')
def authenticate():
    # https://stackoverflow.com/a/33843524
    email = request.headers['email']
    password = request.headers['password']
    query = '''
        SELECT * FROM users WHERE users.email=%s
    '''
    cursor.execute(query, [email])
    res = cursor.fetchall()
    if len(res) == 0:
        # Change status code
        return {'status': 100}
    
    passwordInTable = res[0][7]

    if passwordInTable != password:
        return {'status': 100}
    
    return {'status': 200}

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)