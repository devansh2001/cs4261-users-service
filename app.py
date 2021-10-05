from flask import Flask, request

app = Flask(__name__)

@app.route('/health-check')
def health_check():
    return {'status': 'OK', 'code': '200'}