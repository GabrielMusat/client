import requests
import json
import os
import sys

Artenea_URL = 'http://remotemusat.ddns.net:8000'
default_auth = ('Gabriel', 'contrasenaG')


def home(auth=default_auth):
    try:
        payload = {'instruction': 'home'}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def command(command, auth=default_auth):
    try:
        payload = {'instruction': 'command', 'command': command.upper()}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def print_file(file, auth=default_auth):
    try:
        payload = {'instruction': 'print', 'file': file}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al conectar con el servidor de artenea: ' + str(e))


def register(user, password, auth=default_auth):
    try:
        payload = {user: password}
        r = requests.post(Artenea_URL + '/register', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('no se ha podido registrar nuevo usuario: ' + str(e))


def file_server_to_printer(filename, auth=default_auth):
    try:
        payload = {'instruction': 'download', 'filename': filename}
        r = requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al subir gcode: ' + str(e))


def file_client_to_server(filename, auth=default_auth):
    try:
        file = {'file': open(filename, 'rb')}
        r = requests.post(Artenea_URL + '/upload', files=file, auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print('error al subir gcode a impresora: ' + str(e))


def print3d(filepath, auth=default_auth):
    file_client_to_server(filepath, auth=auth)
    filename = os.path.split(filepath)[1]
    file_server_to_printer(filename, auth=auth)
    print_file(filename, auth=auth)


def give_rights(user, gcode, auth=default_auth):
    try:
        payload = {user: gcode}
        r = requests.post(Artenea_URL + '/rights', data=json.dumps(payload), auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print(f'error al dar derechos del gcode {gcode} a {user}: ' + str(e))


def check_rights(auth=default_auth):
    try:
        r = requests.get(Artenea_URL + '/checkrights', auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print(f'error al checkear derechos: ' + str(e))


def users(auth=default_auth):
    try:
        r = requests.get(Artenea_URL + '/users', auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print(f'error al checkear usuarios registrados: ' + str(e))


def stats(auth=default_auth):
    try:
        r = requests.get(Artenea_URL + '/stats', auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print(f'error al checkear estadísticas: ' + str(e))


def gcodes(auth=default_auth):
    try:
        r = requests.get(Artenea_URL + '/gcodes', auth=auth)
        print(f'{r.status_code}: {r.text}')

    except Exception as e:
        print(f'error al checkear estadísticas: ' + str(e))


if len(sys.argv) > 1 and sys.argv[1] in ['-c', '--command']:
    while True:
        gcode = input('pandora << ').upper()
        if gcode == 'EXIT': exit(0)
        command(gcode)
