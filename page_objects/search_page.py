"""
Проверка расширенного поиска https://www.kinopoisk.ru/s/
"""

from playwright.sync_api import Page
from page_objects.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.year_filter = "input[name='year_from']"  # Пример: фильтр по году
        self.genre_filter = "select[name='m_act[genre]']"  # Пример: фильтр по жанру

    def set_year_filter(self, year_from: str, year_to: str):
        """Установить фильтр по году."""
        self.page.fill(self.year_filter, year_from)
        self.page.fill("input[name='year_to']", year_to)

    def select_genre(self, genre: str):
        """Выбрать жанр из выпадающего списка."""
        self.page.select_option(self.genre_filter, genre)