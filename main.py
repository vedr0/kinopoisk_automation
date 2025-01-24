# from playwright.sync_api import sync_playwright
#
# def save_browser_state():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#
#         # Зайти на сайт и авторизоваться
#         page.goto("https://www.kinopoisk.ru/")
#         input("Пройдите авторизацию вручную и нажмите Enter...")
#
#         # Сохранить состояние
#         context.storage_state(path="storage_state.json")
#         print("Состояние сохранено в storage_state.json")
#
#         browser.close()
#
# save_browser_state()