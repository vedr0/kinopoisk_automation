import pytest
from playwright.sync_api import Page, expect
from utils.form_interaction import fill_field, select_field, select_genres, fill_creator_pair

class AdvancedSearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.kinopoisk.ru/s/"
        self.form_f1 = page.locator("form[name='film_search']")
        self.form_f2 = page.locator("form[name='keyword_search']")
        self.search_button_f1 = self.form_f1.locator(".el_18.submit.nice_button")
        self.search_button_f2 = page.locator("#btn_search_6")

    def open(self):
        self.page.goto(self.url, wait_until="load")
        self.page.wait_for_selector("form[name='film_search']", timeout=30000)
        self.page.wait_for_selector("form[name='keyword_search']", timeout=30000)

    def fill_form_f1(self, test_case: dict):
        # Вызываем функции из form_interaction с mode='f1'
        fill_field(self.page, "f1", "m_act[find]", test_case["Название фильма"])
        fill_field(self.page, "f1", "m_act[year]", test_case["Год"])
        fill_field(self.page, "f1", "m_act[box]", test_case["Сумма сборов"])
        fill_field(self.page, "f1", "m_act[actor]", test_case["Актер"])
        fill_field(self.page, "f1", "m_act[cast]", test_case["Создатели"])

        select_field(self.page, "f1", "m_act[from_year]", test_case["Начало интервала годов"])
        select_field(self.page, "f1", "m_act[to_year]", test_case["Конец интервала годов"])
        select_field(self.page, "f1", "m_act[country]", test_case["Страна"])
        select_field(self.page, "f1", "m_act[company]", test_case["Прокатчик"])
        select_field(self.page, "f1", "m_act[mpaa]", test_case["MPAA рейтинг"])
        select_field(self.page, "f1", "m_act[premier_month]", test_case["Месяц премьеры"])
        select_field(self.page, "f1", "m_act[premier_year]", test_case["Год премьеры"])
        select_field(self.page, "f1", "m_act[premier_type]", test_case["Регион премьеры"])
        select_field(self.page, "f1", "m_act[box_vector]", test_case["Сравнение сборов"])
        select_field(self.page, "f1", "m_act[box_type]", test_case["Регион сборов"])
        select_field(self.page, "f1", "m_act[content_find]", test_case["Что искать?"])

        if test_case["Жанр"] and test_case["Жанр"] != "-":
            genres = [g.strip() for g in test_case["Жанр"].split(",")]
            select_genres(self.page, "f1", genres)

    def fill_form_f2(self, test_case: dict):
        index = 1
        while True:
            role_key = f"Роль {index}"
            name_key = f"Имя {index}"
            if role_key not in test_case and name_key not in test_case:
                break
            role = test_case.get(role_key, "").strip()
            name = test_case.get(name_key, "").strip()
            if not role and not name:
                break
            fill_creator_pair(self.page, index, role, name)
            index += 1

    def submit_f1(self):
        if not self.search_button_f1.is_enabled():
            pytest.xfail("❌ Кнопка поиска неактивна")
        self.search_button_f1.click()
        self.page.wait_for_load_state("load")

    def submit_f2(self):
        if not self.search_button_f2.is_enabled():
            pytest.xfail("❌ Кнопка поиска неактивна")
        self.search_button_f2.click()
        self.page.wait_for_load_state("load")