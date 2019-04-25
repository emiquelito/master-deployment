#!/usr/bin/env python3
from flask import Flask, request
import threading
import time
import logging
import requests
import os

app = Flask(__name__)


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            # logging.warning("Run recurring task")
            time.sleep(0.25)

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def index():
    logging.warning(request.referrer)
    master_url = os.environ.get('SQUASH_MASTER_DEPLOYMENT')
    if not master_url:
        return '<body><h2>Master deployment URL is not defined</h2></body>'
    if 'https' not in master_url:
        master_url = f'https:{master_url}'
    try:
        resp = requests.get(master_url)
        if resp.status_code != 200:
            return f'<body><h3>Master deployment URL {master_url} is unreachable</h3></body>'
    except Exception:
        return f'<body><h3>Master deployment URL {master_url} is unreachable</h3></body>'

    return f'<body><h1>Received success response from {master_url}</h1></body>'


@app.route('/child/')
def about():
    logging.warning(request.referrer)
    child_url = os.environ.get('SQUASH_CHILD_DEPLOYMENT')
    if not child_url:
        return '<body><h2>CHILD deployment URL is not defined</h2></body>'
    if 'https' not in child_url:
        child_url = f'https:{child_url}'
    try:
        resp = requests.get(child_url)
        if resp.status_code != 200:
            return f'<body><h3>Child deployment URL {child_url} is unreachable</h3></body>'
    except Exception:
        return f'<body><h3>Child deployment URL {child_url} is unreachable</h3></body>'

    return f'<body><h1>Received success response from Child Deployment {child_url}</h1></body>'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
