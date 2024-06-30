import json
from services.user_svc import UserSvc


def parse_json(body):
    return json.loads(body) if body else None

def send_json_response(handler, data):
    response_body = json.dumps(data)
    handler.send_response(200, 'OK', response_body)


class UserController:
    def __init__(self):
        self.user_svc = UserSvc()

    def do_POST(self, handler, path, headers, body):
        if path == '/users/register':
            self.handle_register(handler, body)
        elif path == '/users/login':
            self.handle_login(handler, body)
        elif path == '/users/create_personal_bank':
            self.handle_create_personal_bank(handler, body)
        elif path == '/users/create_vaquita':
            self.handle_create_vaquita(handler, body)
        elif path == '/users/join_vaquita':
            self.handle_join_vaquita(handler, body)
        else:
            handler.send_response(404, 'Not Found')
            handler.end_headers()

    def do_GET(self, handler, path, headers, body):
        if path == '/users':
            self.handle_get_all_users(handler)
        elif path.startswith('/users/accounts/'):
            self.handle_get_user_accounts(handler, path)
        else:
            handler.send_response(404, 'Not Found')
            handler.end_headers()

    def handle_register(self, handler, body):
        data = parse_json(body)
        if data:
            user_id = self.user_svc.register(data['name'], data['email'], data['password'])
            send_json_response(handler, {'user_id': user_id})

    def handle_login(self, handler, body):
        data = parse_json(body)
        if data:
            user_id = self.user_svc.login(data['email'], data['password'])
            send_json_response(handler, {'user_id': user_id})

    def handle_get_all_users(self, handler):
        users = self.user_svc.get_all_users()
        send_json_response(handler, users)

    def handle_create_personal_bank(self, handler, body):
        data = parse_json(body)
        if data:
            self.user_svc.create_personal_bank(data['bank_name'], data['bank_balance'], data['user_id'], data['password'])
            send_json_response(handler, {'message': 'Bank created'})

    def handle_join_vaquita(self, handler, body):
        data = parse_json(body)
        if data:
            result = self.user_svc.join_vaquita(data['user_id'], data['vaquita_number'], data['password'])
            send_json_response(handler, {'result': result})

    def handle_get_user_accounts(self, handler, path):
        user_id = int(path.split('/')[-1])
        accounts = self.user_svc.get_user_accounts(user_id)
        send_json_response(handler, accounts)

    def handle_create_vaquita(self, handler, body):
        data = parse_json(body)
        if data:
            self.user_svc.create_personal_bank(data['bank_name'], data['bank_balance'], data['user_id'], data['password'], personal=False)
            send_json_response(handler, {'message': 'Vaquita created'})
