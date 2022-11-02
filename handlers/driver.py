from handlers.user import method_info_handler
from handlers.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep


def method_handler(driver, data):  # функция, которая обрабатывает выбранный метод
    # попытка авторизации
    try:
        auth_handler(driver, data)

    except Exception as ex:
        print(ex)
        print("Пользователь уже авторизован\n...")

    if data.method == 0:
        data.method = method_info_handler()

    last_homework_info_handler = Config(param="last_homework_info")

    if data.method["type"] == "path":  # обработка первого метода
        courses_list_handler = Config(param="courses_list")

        courses_list = courses_list_handler.get()
        course_form = driver.find_element(By.ID, 'course_id')

        full_courses_list = list(map(lambda elem: elem.text, course_form.find_elements(By.TAG_NAME, "option")))[1:]
        if not courses_list:
            print(" - Конфигурационный файл, содержащий названия курсов пуст...\n"
                  " - Выберите курсы из списка, которые нужно добавить:\n")
            for i in range(len(full_courses_list)):
                print(f"    {i + 1}. {full_courses_list[i]}")
            print(" - Введите номера ")
            full_courses_list_indexes = list(
                map(int, input(" - Введите номера курсов через пробел (пример: 1 4 3): ").split()))
            # защита от дурака + обработка индекса
            full_courses_list_indexes_new = [index - 1 for index in list(set(full_courses_list_indexes)) if
                                             0 <= index - 1 < len(full_courses_list)]
            courses_list = list(map(lambda index: full_courses_list[index], full_courses_list_indexes_new))
            courses_list_handler.add(courses_list)

        while not (1 <= (action := int(input(" - Выберите действие:\n"
                                             "     1. Выбрать курс\n"
                                             "     2. Изменить список курсов\n"
                                             " - Выберите номер элемента: "))) <= 2):
            print("Ошибка: Введено неверное значение")

        if action == 2:
            pass
        else:
            print(" - Выберите курс:")
            for i in range(len(courses_list)):
                print(f"    {i + 1}. {courses_list[i]}")
            # защита от дурака
            while not (0 <= (course_index := int(input(" - Введите номер выбранного элемента: ")) - 1) < len(courses_list)):
                print("Ошибка: Введено неверное значение")
            Select(course_form).select_by_visible_text(courses_list[course_index])
            sleep(.5)

            module_form = driver.find_element(By.ID, 'module_id')
            module_list = list(map(lambda elem: elem.text, module_form.find_elements(By.TAG_NAME, "option")))[1:]
            print(" - Выберите блок:")
            for i in range(len(module_list)):
                print(f"    {i + 1}. {module_list[i]}")
            # защита от дурака
            while not (0 <= (block_index := int(input(" - Введите номер выбранного элемента: ")) - 1) < len(module_list)):
                print("Ошибка: Введено неверное значение")
            Select(module_form).select_by_visible_text(module_list[block_index])
            sleep(.5)

            lesson_form = driver.find_element(By.ID, 'lesson_id')
            lesson_list = list(map(lambda elem: elem.text, lesson_form.find_elements(By.TAG_NAME, "option")))[1:]
            print(" - Выберите урок:")
            for i in range(len(lesson_list)):
                print(f"    {i + 1}. {lesson_list[i]}")
            # защита от дурака
            while not (0 <= (lesson_index := int(input(" - Введите номер выбранного элемента: ")) - 1) < len(lesson_list)):
                print("Ошибка: Введено неверное значение")
            Select(lesson_form).select_by_visible_text(lesson_list[lesson_index])
            sleep(.5)

            submit_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/section/div/div/div/div/'
                                                          'div[1]/div/form/div[2]/button')
            submit_button.click()

            data.method = {
                "type": "link",
                "link": driver.current_url
            }

            last_homework_info_handler.add({
                "name": lesson_list[lesson_index],
                "link": data.method["link"]
            })

    elif data.method["type"] == "link":
        driver.get(data.method["link"])
        sleep(2)
        last_homework_info_handler.add({
            "name": driver.find_element(By.CSS_SELECTOR, "#lesson_id option[selected]").text,
            "link": data.method["link"]
        })

    sleep(3)


def auth_handler(driver, data):
    while True:
        try:
            login_input = driver.find_element(By.XPATH, '//*[@id="email"]')
            passwd_input = driver.find_element(By.XPATH, '//*[@id="password"]')
            remember_me = driver.find_element(By.XPATH, '//*[@id="remember_me"]')
            auth_button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[4]/button')

        except Exception as ex:
            print(ex)
            print("...\nПользователь успешно авторизован\n...")
            break
        else:
            login_input.send_keys(data.login)
            passwd_input.send_keys(data.password)
            remember_me.click()
            sleep(1)

            auth_button.click()
            sleep(3)
            driver.refresh()
