from playwright.sync_api import sync_playwright
import time

BASE_URL = "http://127.0.0.1:5000"

USERNAME = "MOPSAR"
PASSWORD = "Mopsik123!"


def login(page):
    page.goto(BASE_URL)

    # 2 инпута на странице: User и Password
    inputs = page.locator("input")
    inputs.nth(0).fill(USERNAME)
    inputs.nth(1).fill(PASSWORD)

    # Кликаем по настоящей кнопке Login
    page.get_by_role("button", name="Login").click()

    page.wait_for_load_state("networkidle")
    # Проверяем, что действительно вошли
    page.get_by_text("Add Tasks", exact=False).is_visible()

# ТЕСТ №2: Добавление задачи
def test_add_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Логинимся
        login(page)

        # Переходим на Add Tasks
        page.get_by_text("Add Tasks", exact=False).click()
        page.wait_for_load_state("networkidle")

        # Вводим текст задачи
        task_text = f"E2E task {int(time.time())}"

        task_input = page.locator("input").nth(0)
        task_input.fill(task_text)

        # Жмём кнопку добавления задачи
        page.get_by_role("button", name="Add Task").click()

        # Проверяем, что задача появилась в списке справа
        assert page.get_by_text(task_text, exact=False).is_visible()

        page.locator("span.menu").click()

        # Кликаем "View Tasks" в выпавшем меню
        page.get_by_role("link", name="View Tasks").click()
        page.wait_for_load_state("networkidle")

        # Проверяем, что наша задача есть и на странице View Tasks
        assert page.get_by_text(task_text, exact=False).is_visible()

        browser.close()
