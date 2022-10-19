import json


def get_method() -> list:
    while ((method := int(input("Методы:\n"
                                "   1) Путь до урока\n"
                                "   2) Ссылка на урок\n"
                                "Введите номер метода: "))) not in [1, 2]):
        print("Введите валидное значение..")

    if method == 1:
        path = str(input("Введите путь (Формат: Курс/Модуль/Домашка) (Названия строго, как на сайте): ")).split("/")
        return [method, path]
    else:
        link = str(input("Введите ссылку: "))
        return [method, link]


def json_handler():
    with open("misc/auth_data.json") as json_file:
        data = json.load(json_file)

    if data["login"] != "" and data["password"] != "" and \
            int(input("Вы уже авторизованы, если хотите сбросить данные, нажмите 1, иначе 0: ")) == 1 \
            or data["login"] == "" or data["password"] == "":
        login = str(input("Введите логин: "))
        password = str(input("Введите пароль: "))

        while int(input("Если данные введены верно нажмите 1, иначе 0: ")) == 0:
            login = str(input("Введите логин: "))
            password = str(input("Введите пароль: "))

        with open("misc/auth_data.json", 'w') as json_file:
            data["login"], data["password"] = login, password
            json.dump(data, json_file)
    return data["login"], data["password"]
