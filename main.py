from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from config import Auth, json_handler


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


def parse(driver):
    cnt = 0
    # проходимся по всем домашним работам
    while len((table_rows := driver.find_element(By.XPATH, '//*[@id="example2"]/tbody').find_elements(By.TAG_NAME,
                                                                                                      'tr'))) != 0:
        row = table_rows[0]

        preview_button = row.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')

        student_name = row.find_elements(By.TAG_NAME, 'td')[2].find_element(By.TAG_NAME, 'div').text
        homework_link = preview_button.get_attribute("href")

        preview_button.click()
        sleep(1)

        print(f"Имя студента, чья работа проверяется: {student_name}\n"
              f"Ссылка на работу: {homework_link}")

        try:
            start_checking_btn = driver.find_element(By.ID, 'blockHomework')
            start_checking_btn.click()
            print(' - Нажата кнопка "Начать проверку"')
            sleep(2)
        except Exception as ex:
            print(' - Кнопка "Начать проверку" уже нажата')
            print(ex)

        div_blocks = driver.find_elements(By.CSS_SELECTOR, "div.tab-pane>div")

        # проходимся по всем заданиям
        for i in range(2, len(div_blocks), 3):
            print(f" - Задание №{i // 3 + 1}")
            admin_area = div_blocks[i].find_elements(By.XPATH, './*')

            checkbox = admin_area[0].find_element(By.XPATH, './label')
            comment_area = admin_area[2].find_element(By.CSS_SELECTOR, '.note-editing-area>.card-block')
            save_answer_btn = admin_area[2].find_elements(By.XPATH, './div')[-1].find_element(By.TAG_NAME, 'button')

            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            sleep(.5)
            checkbox.click()
            print('     - Нажата кнопка "Проверено дежурным куратором"')

            driver.execute_script("arguments[0].scrollIntoView();", comment_area)
            sleep(.5)
            comment_area.send_keys("Работа отправлена на проверку твоему куратору")
            print('     - Добавлен комментарий к заданию')

            driver.execute_script("arguments[0].scrollIntoView();", save_answer_btn)
            sleep(.5)
            save_answer_btn.click()
            print('     - Ответ сохранен')

            sleep(.5)

        apply_btn = driver.find_element(By.CSS_SELECTOR, '#decision_buttons>button:first-child')
        apply_btn.click()
        sleep(2)

        apply_confirm_btn = driver.find_element(By.ID, 'applyBtn')
        apply_confirm_btn.click()
        sleep(2)
        print(" - Домашняя работа принята\n"
              " - Проверка домашней работы завершена")

        for _ in range(3):
            driver.back()
            sleep(.3)

        cnt += 1
        print(f"Кол-во успешно обработанных домашних работ: {cnt}\n...")

        driver.refresh()
        sleep(2)


def method_handler(driver, method: list, login: str, password: str):
    if method[0] == 1:
        driver.get("https://api.100points.ru/exchange/index")
    elif method[0] == 2:
        driver.get(method[1])

    login_input = driver.find_element(By.XPATH, '//*[@id="email"]')
    passwd_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    remember_me = driver.find_element(By.XPATH, '//*[@id="remember_me"]')

    login_input.send_keys(login)
    passwd_input.send_keys(password)
    remember_me.click()
    sleep(1)

    auth_button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[4]/button')
    auth_button.click()
    print("...\nПользователь успешно авторизован\n...")
    sleep(3)
    # обработка первого метода
    if method[0] == 1:
        path = method[1]

        course_form = Select(driver.find_element(By.ID, 'course_id'))
        course_form.select_by_visible_text(path[0])
        sleep(.5)

        module_form = Select(driver.find_element(By.ID, 'module_id'))
        module_form.select_by_visible_text(path[1])
        sleep(.5)

        lesson_form = Select(driver.find_element(By.ID, 'lesson_id'))
        lesson_form.select_by_visible_text(path[2])
        sleep(.5)

        submit_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/section/div/div/div/div/'
                                                      'div[1]/div/form/div[2]/button')
        submit_button.click()
        sleep(3)

    sleep(3)


def main():
    json_handler()
    login, password = Auth.login, Auth.password

    method = get_method()
    driver = webdriver.Chrome()

    try:
        method_handler(driver=driver, method=method, login=login, password=password)
        parse(driver=driver)

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
