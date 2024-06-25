import json

from services.user_svc import UserSvc


class UserController:
    def __init__(self):
        self.user_svc = UserSvc()

    def do_POST(self, handler):
        if handler.path == '/users/register':
            self.handle_register(handler)
        elif handler.path == '/users/login':
            self.handle_login(handler)
        elif handler.path == '/users/create_personal_bank':
            self.handle_create_personal_bank(handler)
        elif handler.path == '/users/create_vaquita':
            self.handle_create_vaquita(handler)
        elif handler.path == '/users/join_vaquita':
            self.handle_join_vaquita(handler)
        else:
            handler.send_response(404)
            handler.end_headers()

    def do_GET(self, handler):
        if handler.path == '/users':
            self.handle_get_all_users(handler)
        elif handler.path.startswith('/users/accounts/'):
            self.handle_get_user_accounts(handler)
        else:
            handler.send_response(404)
            handler.end_headers()

    def handle_register(self, handler):
        data = json.loads(handler.rfile.read(int(handler.headers['Content-Length'])))
        user_id = self.user_svc.register(data['name'], data['email'], data['password'])
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps({'user_id': user_id}).encode())

    def handle_login(self, handler):
        data = json.loads(handler.rfile.read(int(handler.headers['Content-Length'])))
        user_id = self.user_svc.login(data['email'], data['password'])
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps({'user_id': user_id}).encode())

    def handle_get_all_users(self, handler):
        users = self.user_svc.get_all_users()
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(users).encode())

    def handle_create_personal_bank(self, handler):
        data = json.loads(handler.rfile.read(int(handler.headers['Content-Length'])))
        self.user_svc.create_personal_bank(data['bank_name'], data['bank_balance'], data['user_id'], data['password'])
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps({'message': 'Bank created'}).encode())

    def handle_join_vaquita(self, handler):
        data = json.loads(handler.rfile.read(int(handler.headers['Content-Length'])))
        result = self.user_svc.join_vaquita(data['user_id'], data['vaquita_number'], data['password'])
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps({'result': result}).encode())

    def handle_get_user_accounts(self, handler):
        user_id = int(handler.path.split('/')[-1])
        accounts = self.user_svc.get_user_accounts(user_id)
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(accounts).encode())

    def handle_create_vaquita(self, handler):
        data = json.loads(handler.rfile.read(int(handler.headers['Content-Length'])))
        self.user_svc.create_personal_bank(data['bank_name'], data['bank_balance'], data['user_id'], data['password'], personal=False)
        handler.send_response(200)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps({'message': 'Vaquita created'}).encode())
