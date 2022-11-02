from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from dataclasses import dataclass
from time import sleep
from handlers.user import auth_info_handler
from handlers.driver import *


@dataclass()
class Data:  # наследуется класс data, внутри которого вся нужная информация
    login: str
    password: str
    method: dict = 0
    k: int = 0
    cnt: int = 0


def parse(driver, data):  # parsing функция
    # проходимся по всем домашним работам
    while hw_cnt := len((table_rows := driver.find_element(By.XPATH, '//*[@id="example2"]/tbody').find_elements(
            By.TAG_NAME, 'tr'))) != 0:

        # защита: если кол-во работ больше числа k
        if data.k > hw_cnt:
            data.k = 0

        row = table_rows[data.k]

        preview_button = row.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')

        student_name = row.find_elements(By.TAG_NAME, 'td')[2].find_element(By.TAG_NAME, 'div').text
        homework_link = preview_button.get_attribute("href")

        preview_button.click()
        sleep(1)

        # исключение домашняя работа уже проверяется / домашняя работа проверяется другим куратором
        try:
            start_checking_btn = driver.find_element(By.ID, 'blockHomework')
            start_checking_btn.click()
            print(' - Нажата кнопка "Начать проверку"')
            print(f"Имя студента, чья работа проверяется: {student_name}\n"
                  f"Ссылка на работу: {homework_link}")
            sleep(2)
        except Exception as ex:  # исключение: домашняя работа уже проверяется
            try:
                active_hw_btn = driver.find_element(By.CSS_SELECTOR, ".alert>a")
                active_hw_btn.click()
                print(" - Ошибка: Уже проверяется другая домашняя работа")
                print(ex)
                sleep(2)

                driver.find_element(By.ID, 'unblockHomework').click()
                sleep(.5)

                starter(driver, data)
            except Exception as ex:  # исключение: домашняя работа проверяется другим куратором
                data.k += 1
                print(" - Ошибка: Работа проверяется другим куратором")
                print(ex)

                starter(driver, data)

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

        data.cnt += 1
        print(f"Кол-во успешно обработанных домашних работ: {data.cnt}\n...")

        driver.refresh()
        sleep(2)


def starter(driver, data, old=0):  # функция с которой parser начинает работу
    try:
        if old == 1:
            driver.get(data.method["link"])
            auth_handler(sources={
                "driver": driver,
                "By": By,
                "sleep": sleep
            }, data=data)
        else:
            driver.get("https://api.100points.ru/exchange/index")
            method_handler(sources={
                "driver": driver,
                "By": By,
                "Select": Select,
                "sleep": sleep
            }, data=data)
        parse(driver, data)
    except Exception as ex:  # исключение: при какой-либо ошибке происходит засыпание и заново запускается функция
        print(f"ОШИБКА - {ex}")
        sleep(60)
        starter(driver, data)


def main():
    login, password = auth_info_handler()
    driver = webdriver.Chrome()
    last_homework_info = Config("last_homework_info").get()
    data = Data(login=login, password=password)

    if last_homework_info != {
        "name": "",
        "link": ""
    }:
        # защита от дурака
        while (old := int(input(f' - Выберите метод запуска:\n'
                                f'   1. Запустить бота\n'
                                f'   2. Продолжить проверку "{last_homework_info["name"]}"\n'
                                f' - Выберите номер элемента: '))) not in [1, 2]:
            print("Ошибка: Введите валидное значение")

        data = Data(login=login, password=password)

        if old == 2:
            data.method = {
                "type": "link",
                "link": last_homework_info["link"]
            }

        starter(driver, data, old - 1)
    else:
        starter(driver, data)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
