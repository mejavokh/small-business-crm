from storage import ClientStorage, OrderStorage
from models import Client, OrderStatus

client_storage = ClientStorage()
order_storage = OrderStorage()

try:
    client_storage.load_from_file()
except FileNotFoundError:
    pass

try:
    order_storage.load_from_file()
except FileNotFoundError:
    pass

def print_clients(clients: list[Client]) -> None:
    if not clients:
        print("Клиент не найден")
    else:
        for client in clients:
            client_id = client.id
            client_name = client.name
            client_phone = client.phone
            print(f"id: {client_id}\n"
                  f"Имя: {client_name}\n"
                  f"Номер телефона: {client_phone}\n--------")

while True:
    print("\n--- Меню ---")
    print("1 - Добавить клиента")
    print("2 - Показать всех клиентов")
    print("3 - Удалить клиента")
    print("4 - Изменить данные клиента")
    print("5 - Найти клиента")
    print("6 - Создать заявку")
    print("7 - Изменить статус заявку")
    print("0 - Выход")

    choice = input("Выберите действие: ")

    if choice == "1":  #add_client
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")

        client_storage.add_client(name=name, phone=phone)
        print("Клиент успешно добавлен!")

    elif choice == "2":  #get_all_clients
        all_clients = client_storage.get_all_clients()

        print_clients(all_clients)

    elif choice == "3":  #delete client
        try:
            client_id_input = int(input("Введите id клиента: "))
            result = client_storage.delete_client(client_id_input)

            if result:
                print("Клиент успешно удален!")
            else:
                print("Клиент с таким id не найден")
        except ValueError:
            print("Идентификатор клиента должен быть числом!")

    elif choice == "4":  #update_client
        try:
            client_id_input = int(input("Введите id клиента: "))
            client_name = input("Введите новое имя клиента: ")
            client_phone = input("Введите новый номер телефона: ")

            name = client_name if client_name != "" else None
            phone = client_phone if client_phone != "" else None

            result = client_storage.update_client(client_id_input, name, phone)

            if result:
                print("Клиент успешно обновлен!")
            else:
                print("Клиент с таким id не найден")
        except ValueError:
            print("Идентификатор клиента должен быть числом!")

    elif choice == "5":  #search_client
        search_query = input("Введите номер или имя клиента для поиска: ")

        results = client_storage.search_clients(search_query)
        print_clients(results)

    elif choice == "6":  #create_order
        try:
            client_id = int(input("Введите id клиента: "))
            client = client_storage.get_client_by_id(client_id)

            if client is None:
                print("Клиент с таким id не найден")
            else:
                date = input("Введите дату заявки")
                description = input("Введите описание для заявки: ")
                status = OrderStatus.PENDING
                order_storage.create_order(client_id, date, description, status)

                print("Заявка успешно создана!")
        except ValueError:
            print("Идентификатор клиента должен быть числом!")

    elif choice == "7":
        try:
            order_id = int(input("Введите id заявки: "))
            status = input("Введите статус заявки(в ожидании, принята, отменена): ")
            new_status = OrderStatus(status)
            result = order_storage.change_status(order_id, new_status)

            if result:
                print("Статус успешно обновлен!")
            else:
                print("Заявка с таким id не найден")

        except ValueError:
            print("Идентификатор клиента должен быть числом,"
                  "а статус - одним из предложенных вариантов!")

    elif choice == "0":  #exit
        break
    else:
        print("Неверный ввод, попробуйте снова")
