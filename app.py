import json
import os
import time

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    api_token = os.getenv('API_TOKEN')
    space_name = os.getenv('SPACE_NAME')
    _file = request.files['file']
    url = f'https://api.digitalocean.com/v2/spaces/{space_name}'
    headers = {'Content-Type': 'application/octet-stream', 'Authorization': f'Bearer {api_token}'}

    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, data=_file)
    except requests.exceptions.RequestException as e:
        return f'Error: {e}'
    end_time = time.time()

    content = {'status_code': response.status_code}

    if response.status_code == 200:
        response_data = json.loads(response.content)
        upload_time = end_time - start_time
        content['file_name'] = request.files['file'].filename
        content['file_url'] = response_data['data']['links']['public']
        content['upload_time'] = f'{upload_time:.2f}'
        content['last_modified'] = response_data['data']['last_modified']
    else:
        content['error'] = response.content

    return render_template('result.html', content=content)


if __name__ == '__main__':
    app.run()
