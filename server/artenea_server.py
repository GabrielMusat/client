from flask import Flask, request, send_file
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from OpenSSL import SSL
import utils
import json
import os

config = json.loads(open('artenea_server.conf').read())
users = json.loads(open('UsersDDBB.conf').read())
admins = json.loads(open('AdminsDDBB.conf').read())

#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('yourserver.key')
#context.use_certificate_file('yourserver.crt')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth_user = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()

buffer = {}
for user_name in users:
    buffer[user_name] = []


@auth_user.get_password
def get_pw(username):
    if username in users:
        return users[username]
    return None


@auth_admin.get_password
def get_pw(username):
    if username in admins:
        return admins[username]
    return None


@app.route('/')
@auth_admin.login_required
def test():
    return 'ok'


@app.route('/register', methods=['POST'])
@auth_admin.login_required
@cross_origin()
def register():
    try:
        new_users = json.loads(request.data)
        for new_user in new_users:
            if new_user in users:
                print('user already registered')
            else:
                users[new_user] = new_users[new_user]
                buffer[new_user] = []
                with open('UsersDDBB.conf', 'w') as UsersDDBB:
                    UsersDDBB.write(json.dumps(users, indent=4))

                print(f'new user {new_user} registered correctly')

        return 'ok'

    except Exception as e:
        print('new user registration failed')
        print(e)

        return 'failed'


@app.route('/users', methods=['POST'])
@cross_origin()
def users():
    return json.dumps(users, indent=4)


@app.route('/buffer', methods=['GET'])
@auth_user.login_required
@cross_origin()
def return_buffer():
    global buffer
    user = auth_user.username()

    if len(buffer[user]) > 0:
        to_return = buffer[user][0]
        print('sending instruction and deleting it from buffer')
        del buffer[user][0]
        return to_return

    else:
        return json.dumps({'instruction': 'None'})


@app.route('/add', methods=['POST'])
@auth_user.login_required
@cross_origin()
def add_to_buffer():
    global buffer
    try:
        json_instruction = request.data
        user = auth_user.username()
        buffer[user].append(json_instruction)
        print('json added to buffer')
        return json.dumps({'status': 'ok'})

    except Exception as e:
        print('error adding instruction to buffer:')
        print(e)
        return json.dumps({'status': 'could not add instruction to buffer', 'error': str(e)})


@app.route('/upload', methods=['POST'])
@auth_user.login_required
@cross_origin()
def upload_file():
    try:
        user = auth_user.username()
        folder = 'users/' + user + '/uploads'
        file = request.files['file']
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'gcode':
            utils.maybe_create(folder)
            file.save(os.path.join(folder, file.filename))
            return json.dumps({'status': 'gcode uploaded correctly'})

        else:
            return json.dumps({'status': 'not a gcode'})

    except Exception as e:
        print('error al subir gcode:')
        print(e)
        return json.dumps({'status': 'error uploading gcode', 'error': str(e)})


@app.route('/download', methods=['GET'])
@auth_user.login_required
@cross_origin()
def download_file():
    try:
        user = auth_user.username()
        filename = request.args.get('filename')
        folder = 'users/' + user + '/uploads'
        return send_file(folder + '/' + filename)

    except Exception as e:
        print('error al mandar gcode a impresora:')
        print(e)
        return json.dumps({'file': 'None'})


if __name__ == '__main__':
    app.run(host=config['Artenea_host'], port=config['Artenea_port'])
