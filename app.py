from logging import debug
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/health-check')
def health_check():
    return {'status': 'OK', 'code': '200'}

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)