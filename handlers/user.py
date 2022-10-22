import json


def method_info_handler() -> dict:  # обработчик метода перехода к домашней работе
    # защита от дурака
    while ((method := int(input("Методы:\n"
                                "   1) Путь до урока\n"
                                "   2) Ссылка на урок\n"
                                "Введите номер метода: "))) not in [1, 2]):
        print("Введите валидное значение..")

    return {
        "type": "path"
    } if method == 1 else {
        "type": "link",
        "link": str(input("Введите ссылку: "))
    }


def auth_info_handler():  # обработчик логина и пароля
    with open("misc/config.json") as json_file:
        data = json.load(json_file)

    auth_info = data["auth_info"][0]

    if auth_info["login"] != "" and auth_info["password"] != "" and \
            int(input("Вы уже авторизованы, если хотите сбросить данные, нажмите 1, иначе 0: ")) == 1 \
            or auth_info["login"] == "" or auth_info["password"] == "":  # если пользователь хочешь сбросить данные или данных нет
        login = str(input("Введите логин: "))
        password = str(input("Введите пароль: "))

        while int(input("Если данные введены верно нажмите 1, иначе 0: ")) == 0:
            login = str(input("Введите логин: "))
            password = str(input("Введите пароль: "))

        auth_info["login"], auth_info["password"] = login, password
        data["auth_info"] = auth_info

        with open("misc/auth_data.json", 'w') as json_file:  # запись новых данных в файл
            json.dump(data, json_file, indent=4)
    return auth_info["login"], auth_info["password"]
