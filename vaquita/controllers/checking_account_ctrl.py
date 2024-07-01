# checking_account_controller.py
import json
from services.checking_account_svc import CheckingAccountSvc


def parse_json(body):
    return json.loads(body) if body else None


def send_json_response(handler, data):
    response_body = json.dumps(data)
    handler.send_response(200, "OK", response_body)


# server.py
def notify_clients(handler, account_id, transaction):
    from server import MainServer

    if account_id in MainServer.connected_clients:
        for client in MainServer.connected_clients[account_id]:
            response = (
                json.dumps(
                    {
                        "type": "transaction_update",
                        "account_id": account_id,
                        "transaction": transaction.to_dict(),
                    }
                ).encode("utf-8")
                + b"\n"
            )
            try:
                client.wfile.write(response)
                client.wfile.flush()
                print(f"Sent update to client {client.client_address[0]}: {response}")
            except Exception as e:
                print(
                    f"Failed to send update to client {client.client_address[0]}: {e}"
                )


class CheckingAccountController:
    def __init__(self):
        self.checking_account_svc = CheckingAccountSvc()

    def do_GET(self, handler, path, headers, body):
        if path.startswith("/checking_accounts/transactions"):
            self.handle_get_transactions(handler, path)
        else:
            handler.send_response(404)
            handler.end_headers()

    def do_POST(self, handler, path, headers, body):
        if path == "/checking_accounts/transactions/add":
            self.handle_add_transaction(handler, body)
        else:
            handler.send_response(404)
            handler.end_headers()

    def handle_add_transaction(self, handler, body):
        data = parse_json(body)
        if data:
            try:
                transaction = self.checking_account_svc.add_transaction(
                    account_id=data["account_id"],
                    amount=data["amount"],
                    transaction_type=data["transaction_type"],
                    category=data["category"],
                    notes=data.get("notes", ""),
                    recurring=data.get("recurring", False),
                    description=data["description"],
                    user_id=data["user_id"],
                )
                send_json_response(
                    handler, {"message": "Transaction added successfully"}
                )
                notify_clients(handler, data["account_id"], transaction)
            except ValueError as e:
                send_json_response(handler, {"error": str(e)})
            except Exception as e:
                send_json_response(handler, {"error": "Internal server error"})
                raise e
        else:
            send_json_response(handler, {"error": "Invalid data"})

    def handle_get_transactions(self, handler, path):
        try:
            account_id = int(path.split("/")[-1])
            transactions = self.checking_account_svc.get_transactions(account_id)
            transactions_dict = [transaction.to_dict() for transaction in transactions]
            send_json_response(handler, transactions_dict)
        except ValueError as e:
            send_json_response(handler, {"error": str(e)})
        except Exception as e:
            send_json_response(handler, {"error": "Internal server error"})
            raise e
