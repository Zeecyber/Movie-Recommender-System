from flask import Flask, request, jsonify, render_template,redirect,url_for
import utility_fun
import requests

utility_fun.app
utility_fun.app.secret_key

SUB_SERVER_URLS = {
    'user_management': 'http://127.0.0.1:5001',
    'recommendation': 'http://127.0.0.1:5002',
    'admin_dashboard': 'http://127.0.0.1:5003'
}

@utility_fun.app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@utility_fun.app.route('/signup', methods=['GET', 'POST'])
def signup():
    url = "http://127.0.0.1:5001/signup"
    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    else:
        response = requests.post(url, json=request.get_json())

    return jsonify(response.json()), response.status_code


@utility_fun.app.route('/signin', methods=['GET', 'POST'])
def signin():
    url = "http://127.0.0.1:5001/signin"
    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    else:
        response = requests.post(url, json=request.get_json())

    return  response.status_code


if __name__ == "__main__":
    utility_fun.app.run(debug=True, port=5000)


"""

@app.route('/<sub_server>/<path:endpoint>', methods=['GET', 'POST'])
def route_to_sub_server(sub_server, endpoint):
    if sub_server not in SUB_SERVER_URLS:
        return jsonify({"error": "Invalid sub-server"}), 404

    sub_server_url = SUB_SERVER_URLS[sub_server]
    url = f"{sub_server_url}/{endpoint}"

    if request.method == 'GET':
        response = requests.get(url, params=request.args)
    else:
        response = requests.post(url, json=request.get_json())

    return jsonify(response.json()), response.status_code

"""