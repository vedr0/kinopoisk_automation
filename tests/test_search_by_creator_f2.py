import pytest
import allure
import csv
from playwright.sync_api import Page
from utils.page_analysis import analyze_result_page
from page_objects.advanced_search_page import AdvancedSearchPage


def load_test_data():
    test_data = []
    with open("test_data/f2_creator_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            test_data.append(row)
    return test_data


@pytest.mark.f2
@pytest.mark.parametrize("test_case", load_test_data())
@allure.title("Тест формы поиска по создателям (f2)")
@allure.description("Форма f2: проверка работы автокомплита и комбинаций ролей + имён")
def test_search_by_creator_f2(page: Page, test_case):
    search_page = AdvancedSearchPage(page)
    search_page.open()

    print(f"\n🧪 Запуск теста f2 с параметрами: {test_case}")

    search_page.fill_form_f2(test_case)
    search_page.submit_f2()

    analyze_result_page(page, test_case, mode="f2")
