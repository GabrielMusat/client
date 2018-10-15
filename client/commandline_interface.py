import requests
import json

Artenea_URL = 'http://192.168.1.53:8000'
auth = ('Jose Luis', 'contrasenaJL')


def home():
    try:
        payload = {'instruction': 'home'}
        requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print('Usuario aprieta el boton home desde su ordenador a traves de la pagina web de Artenea')

    except Exception as e:
        print('error al conectar con el servidor de artenea:')
        print(e)


def print_file(file):
    try:
        payload = {'instruction': 'print', 'file': file}
        requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print('Usuario pide que se imprima su modelo llamado "{}"'.format(file))

    except Exception as e:
        print('error al conectar con el servidor de artenea:')
        print(e)


def register(user, password):
    try:
        payload = {user: password}
        requests.post(Artenea_URL + '/register', data=json.dumps(payload), auth=auth)
        print(f'nuevo usuario {user} registrado')

    except Exception as e:
        print('no se ha podido registrar nuevo usuario:')
        print(e)


def upload_file(filename):
    try:
        file = {'file': open(filename, 'rb')}
        payload = {'instruction': 'download', 'filename': filename}
        requests.post(Artenea_URL + '/add', data=json.dumps(payload), auth=auth)
        print('usuario sube un gcode')

    except Exception as e:
        print('error al subir gcode:')
        print(e)

