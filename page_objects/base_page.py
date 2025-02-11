"""
Общая логика для всех страниц
"""

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = "input[name='kp_query']"  # Поле поиска
        self.search_button = "button[aria-label='Найти']"  # Кнопка поиска

    def perform_search(self, query: str):
        """Выполнить поиск по базовому запросу."""
        self.page.fill(self.search_input, query)
        self.page.click(self.search_button)