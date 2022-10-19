def method_handler(sources: dict, data):
    driver = sources["driver"]
    By = sources["By"]
    Select = sources["Select"]
    sleep = sources["sleep"]

    method = data.method
    if method[0] == 1:
        driver.get("https://api.100points.ru/exchange/index")
    elif method[0] == 2:
        driver.get(method[1])

    try:
        login_input = driver.find_element(By.XPATH, '//*[@id="email"]')
        passwd_input = driver.find_element(By.XPATH, '//*[@id="password"]')
        remember_me = driver.find_element(By.XPATH, '//*[@id="remember_me"]')

        login_input.send_keys(data.login)
        passwd_input.send_keys(data.password)
        remember_me.click()
        sleep(1)

        auth_button = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[4]/button')
        auth_button.click()
        print("...\nПользователь успешно авторизован\n...")

    except Exception as ex:
        print(ex)
        print("Пользователь уже авторизован\n...")

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
