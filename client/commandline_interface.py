import requests
import json
import os

Artenea_URL = 'http://remotemusat.ddns.net:8000'
auth = ('Jose Luis', 'contrasenaJL')


def home():
    try:
        payload = {'instruction': 'home'}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def command(command):
    try:
        payload = {'instruction': 'command', 'command': command.upper()}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def print_file(file):
    try:
        payload = {'instruction': 'print', 'file': file}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def register(user, password):
    try:
        payload = {user: password}
        r = requests.post(Artenea_URL + '/register', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('no se ha podido registrar nuevo usuario: ' + str(e))


def file_server_to_printer(filename):
    try:
        payload = {'instruction': 'download', 'filename': filename}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al subir gcode: ' + str(e))


def file_client_to_server(filename):
    try:
        file = {'file': open(filename, 'rb')}
        r = requests.post(Artenea_URL + '/upload', files=file, auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al subir gcode a impresora: ' + str(e))


def print3d(filepath):
    file_client_to_server(filepath)
    filename = os.path.split(filepath)[1]
    file_server_to_printer(filename)
    print_file(filename)
