import os
import json

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():

    data = {
        'ip': request.remote_addr,
        'user_os': request.args.get("os"),
        'browser': request.args.get("browser"),
        'hardwareConcurrency': request.args.get("hc"),
        'gpu': request.args.get("gpu")
    }

    with open(f'saved_data/{data["ip"]}.txt', 'w') as file:
        file.write(json.dumps(data, indent=4))

    return "ok"

def main():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()