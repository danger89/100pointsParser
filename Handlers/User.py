from Handlers.JsonHandler import JsonHandler


def auth_handler() -> tuple:
    json_auth_handler = JsonHandler(param="auth_data")
    login, password = json_auth_handler.read()

    if login is None and password is None \
            or input(" - Вы уже авторизованы, если хотите сбросить данные нажмите 1, иначе 0: ") == "1":
        action = 0
        while action != "1":
            login, password = input(" - Введите логин: "), input(" - Введите пароль: ")
            action = input(" - Если данные введены верно, нажмите 1, иначе 0: ")

        json_auth_handler.write(login=login, password=password)

    return login, password
