import json
from models import Client, Order, OrderStatus
from dataclasses import asdict

class ClientStorage:
    def __init__(self):
        self.filename = "clients.json"
        self.clients = []
        self.next_id = 1

    def add_client(self, name: str, phone: str) -> None:
        new_client = Client(self.next_id, name, phone)
        self.clients.append(new_client)
        self.next_id += 1

        self.save_to_file()

    def delete_client(self, client_id: int) -> bool:
        for existing_client in self.clients:
            if existing_client.id == client_id:
                self.clients.remove(existing_client)
                self.save_to_file()
                return True
        return False

    def update_client(self, client_id: int, name: str | None=None,
                      phone: str | None=None) -> bool:
        for updating_client in self.clients:
            if updating_client.id == client_id:
                if name is not None:
                    updating_client.name = name
                if phone is not None:
                    updating_client.phone = phone
                self.save_to_file()
                return True
        return False

    def search_clients(self, query: str) -> list[Client]:
        result = []
        for searching_client in self.clients:
            if (query in searching_client.name) or (query in searching_client.phone):
                result.append(searching_client)
        return result

    def get_all_clients(self) -> list[Client]:
        return self.clients

    def get_client_by_id(self, client_id: int) -> Client | None:
        for client in self.clients:
            if client.id == client_id:
                return client
        return None

    def save_to_file(self) -> None:
        clients_as_dicts = [asdict(client) for client in self.clients]

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(clients_as_dicts, f, ensure_ascii=False, indent=2)

    def load_from_file(self) -> None:
        with open(self.filename, "r", encoding="utf-8") as f:
            clients_as_dicts = json.load(f)

        self.clients = [Client(**client_dict) for client_dict in clients_as_dicts]

class OrderStorage:
    def __init__(self):
        self.filename = "orders.json"
        self.orders = []
        self.next_order_id = 1

    def create_order(self, client_id: int, date: str,
                     description: str, status: OrderStatus) -> None:
        new_order = Order(self.next_order_id, client_id, date, description, status)
        self.orders.append(new_order)
        self.next_order_id += 1
        self.save_to_file()

    def change_status(self, order_id: int, new_status: OrderStatus) -> bool:
        for order in self.orders:
            if order.order_id == order_id:
                order.status = new_status
                self.save_to_file()
                return True
        return False

    def get_all_orders(self) -> list[Order]:
        return self.orders

    def save_to_file(self) -> None:
        orders_as_dicts = [asdict(order) for order in self.orders]

        for order_dict in orders_as_dicts:
            order_dict["status"] = order_dict["status"].value

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(orders_as_dicts, f, ensure_ascii=False, indent=2)

    def load_from_file(self) -> None:
        with open(self.filename, "r", encoding="utf-8") as f:
            orders_as_dict = json.load(f)

        for order_dict in orders_as_dict:
            order_dict["status"] = OrderStatus(order_dict["status"])

        self.orders = [Order(**order_dict) for order_dict in orders_as_dict]

