from http.server import BaseHTTPRequestHandler
import json
from services.user_svc import UserSvc


class UserController(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.user_svc = UserSvc()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == '/users/register':
            self.handle_register()
        elif self.path == '/users/login':
            self.handle_login()
        elif self.path == '/users/create_personal_bank':
            self.handle_create_personal_bank()
        elif self.path == '/users/join_vaquita':
            self.handle_join_vaquita()
        else:
            self.send_response(404)

    def do_GET(self):
        if self.path == '/users':
            self.handle_get_all_users()
        elif self.path.startswith('/users/accounts/'):
            self.handle_get_user_accounts()
        else:
            self.send_response(404)

    def handle_register(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        user_id = self.user_svc.register(data['name'], data['email'], data['password'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'user_id': user_id}).encode())

    def handle_login(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        user_id = self.user_svc.login(data['email'], data['password'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'user_id': user_id}).encode())

    def handle_get_all_users(self):
        users = self.user_svc.get_all_users()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(users).encode())

    def handle_create_personal_bank(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.user_svc.create_personal_bank(data['bank_name'], data['bank_balance'], data['user_id'], data['password'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Bank created'}).encode())

    def handle_join_vaquita(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        result = self.user_svc.join_vaquita(data['user_id'], data['vaquita_number'], data['password'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'result': result}).encode())

    def handle_get_user_accounts(self):
        user_id = int(self.path.split('/')[-1])
        accounts = self.user_svc.get_user_accounts(user_id)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(accounts).encode())