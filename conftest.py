import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def context_with_auth():
    # Загружаем состояние из файла
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Запускаем браузер
        context = browser.new_context(storage_state="storage_state.json")  # Загружаем storage state
        yield context
        browser.close()
