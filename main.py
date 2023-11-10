from flask import Flask, render_template
import threading
import json
import duolingo_request
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=duolingo_request.make_request, daemon=True).start()
    app.run(host='0.0.0.0', port=3000)