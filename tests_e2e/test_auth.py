from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"

# Данные пользователя
USERNAME = "MOPSAR"
PASSWORD = "Mopsik123!"

# ТЕСТ №1: успешный логин
def test_successful_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # показываем браузер
        page = browser.new_page()

        # Открываем главную страницу
        page.goto(BASE_URL)

        # Заполняем поля "User" и "Password"
        inputs = page.locator("input")
        inputs.nth(0).fill(USERNAME)
        inputs.nth(1).fill(PASSWORD)

        # Нажимаем кнопку "Login"
        page.get_by_role("button", name="Login").click()

        # Ждём загрузки после логина
        page.wait_for_load_state("networkidle")

        # 5. Проверяем, что мы на главной странице после входа:
        assert page.get_by_text("Add Tasks").is_visible()
        assert page.get_by_text(f"Hello! {USERNAME}", exact=False).is_visible()

        # Проверяем, что есть Logout в меню "More"
        page.get_by_text("More..").click()
        assert page.get_by_text("Logout").is_visible()

        browser.close()

# ТЕСТ №3: Некорректный логин
def test_login_with_invalid_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        # вводим неверные данные
        page.locator("input").nth(0).fill("MOPSAR")
        page.locator("input").nth(1).fill("123")

        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("networkidle")

        # на странице должен появиться текст ошибки
        ERROR_TEXT = "invalid Username or Password"
        assert page.get_by_text(ERROR_TEXT, exact=False).is_visible()

        browser.close()


