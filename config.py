from dataclasses import dataclass
import json


@dataclass
class Auth:
    login: str
    password: str


def data_handler(data):
    login = str(input("Введите логин: "))
    password = str(input("Введите пароль: "))

    while int(input("Если данные введены верно нажмите 1, иначе 0: ")) == 0:
        login = str(input("Введите логин: "))
        password = str(input("Введите пароль: "))

    Auth.login, Auth.password = login, password
    data["login"], data["password"] = login, password

    with open("data.json", 'w') as f:
        json.dump(data, f)


def json_handler():
    with open("data.json") as f:
        data = json.load(f)

    if data["login"] == "" and data["password"] == "":
        data_handler(data)
    else:
        data_reset = int(input("Вы уже авторизованы, если хотите сбросить данные, нажмите 1, иначе 0: "))

        if data_reset == 1:
            data_handler(data)
        else:
            Auth.login, Auth.password = data["login"], data["password"]


