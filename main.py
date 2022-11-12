import requests
import fake_useragent
from Handlers.User import auth_handler
from bs4 import BeautifulSoup


def get_browser_data(login, password) -> tuple:
    url = "https://api.100points.ru/login"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

    session = requests.Session()

    headers = {
        "user-agent": user_agent
    }

    data = {
        'email': login,
        'password': password
    }

    session.post(url, data=data, headers=headers)  # response

    cookies = [
        {
            'domain': key.domain,
            'name': key.name,
            'path': key.path,
            'value': key.value
        }
        for key in session.cookies
    ]

    return cookies, headers


def select_homework(headers: dict, cookies: list):  # дописать когда починят сайт
    session = requests.Session()
    exchange_link = 'https://api.100points.ru/exchange/index'

    # добавляем куки файлы
    for cookie in cookies:
        session.cookies.set(**cookie)

    # запрос
    response = session.get(exchange_link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')


class Session:
    def __init__(self, headers, cookies, url):
        self.cookies = cookies
        self.url = url
        self.session = requests.Session()
        self.session.headers = headers

        # добавляем куки файлы
        for cookie in self.cookies:
            self.session.cookies.set(**cookie)

    def get_homework_links(self) -> list:
        homework_links = []

        # запрос
        try:
            response = self.session.get(self.url).text
            soup = BeautifulSoup(response, 'lxml')
        except Exception as ex:
            print(' - Ошибка запроса...')
            print(ex)
        else:
            # получаем все ссылки на домашние работы
            try:
                pages_cnt = int(soup.find_all('li', class_='paginate_button page-item')[-1].text.split()[0])
            except Exception as ex:
                print(" - Что-то пошло не так...")
                print(f" - Проблемный элемент: \n"
                      f"    {soup.find_all('li', class_='paginate_button page-item')}")
                print(ex)
            else:
                print(" - Собираю ссылки на работы учеников...")
                for page in range(1, pages_cnt + 1):
                    try:
                        page_link = f"{self.url}&page={page}"
                        page_response = self.session.get(page_link).text
                        page_soup = BeautifulSoup(page_response, 'lxml')
                    except Exception as ex:
                        print(' - Ошибка запроса...')
                        print(ex)
                    else:
                        try:
                            table_rows = page_soup.find('tbody').find_all('tr')
                        except Exception as ex:
                            print(" - Что-то пошло не так...")
                            print(ex)
                        else:
                            for i in range(len(table_rows)):
                                homework_link = table_rows[i].find_all('td')[0].find('a', href=True)['href']
                                homework_links.append(homework_link)
                print(" - Все ссылки успешно получены\n")
            finally:
                return homework_links

    def start(self):
        # получаем все ссылки на домашние работы
        homework_links = self.get_homework_links()
        count = 0

        # проходимся по всем ссылкам
        for link in homework_links:
            print(f" - Идет обработка домашней работы... \n"
                  f"     Ссылка на работу: {link}")
            try:
                response = self.session.get(link).text
                soup = BeautifulSoup(response, 'lxml')
            except Exception as ex:
                print(' - Ошибка запроса...')
                print(ex)
            else:
                # лист со словарями, которые содержат id кнопки и id формы с комментарием
                id_list = [
                    {
                        'main': button.attrs['id'].split('_')[-1],
                        'textarea': textarea.attrs['id'].split('_')[-1]
                    }
                    for button, textarea in zip(soup.find_all('input', class_='custom-control-input'),
                                                soup.find_all('textarea', class_='form-control comment-form-children'))
                ]

                # данные для post запроса с принятием домашней работы
                apply_link = f"https://api.100points.ru/student_homework/apply/{link.split('/')[-1]}"
                apply_data = {}

                # проходимся по всем id и отправляем post запросы
                for i in range(len(id_list)):
                    id_dict = id_list[i]

                    post_link = f"https://api.100points.ru/student_homework/save_answer/{link.split('/')[-1]}"
                    save_data = {
                        f'is_validate:{id_dict["main"]}': 'on',
                        f'points:{id_dict["main"]}': 1,
                        f'comment:{id_dict["textarea"]}': '<p>Работа отправлена на проверку твоему куратору</p>'
                    }

                    # добавление данных для post запроса с принятием домашней работы
                    for key, value in save_data.items():
                        apply_data[key] = value

                    self.session.post(post_link, data=save_data)
                    print(f"    - Задание №{i + 1} успешно обработано")

                # post запрос для принятия домашней работы
                self.session.post(apply_link, data=apply_data)

            print(" - Работа успешно обработана\n")
            count += 1
            if count % 10 == 0:
                print(f" - Успешно обработанных работ: {count}\n")


def main():
    login, password = auth_handler()
    cookies, headers = get_browser_data(login, password)
    url = input(" - Введите ссылку на урок: ")
    parse_session = Session(headers, cookies, url)

    # запуск скрипта
    parse_session.start()


if __name__ == "__main__":
    main()
