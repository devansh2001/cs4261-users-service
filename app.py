from logging import debug
from flask import Flask, request
import os
import psycopg2

app = Flask(__name__)

# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
def setup():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # https://stackoverflow.com/a/43634941
    conn.autocommit = True

    cursor = conn.cursor()
    try:

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id varchar(64),
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
    
    cursor.execute('INSERT INTO users (fname, lname) VALUES (%s, %s)', ['Devansh', 'Ponda'])
    cursor.execute('INSERT INTO users (fname, lname) VALUES (%s, %s)', ['Tusheet', 'Goli'])
    
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())
    # res = cursor.fetchall()
    # print(res)

    # Check if table exists

setup()

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