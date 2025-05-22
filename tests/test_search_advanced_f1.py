import pytest
import allure
import csv
import time
from playwright.sync_api import Page
from utils.page_analysis import analyze_result_page
from page_objects.advanced_search_page import AdvancedSearchPage


def load_test_data():
    test_data = []
    with open("test_data/f1_advanced_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            test_data.append(row)
    return test_data


@pytest.mark.f1
@pytest.mark.parametrize("test_case", load_test_data())
@allure.title("Тест расширенного поиска фильмов (f1)")
@allure.description("Форма f1: проверка параметров поиска (название, год, жанр, страна и пр.)")
def test_advanced_search_f1(page: Page, test_case):
    search_page = AdvancedSearchPage(page)
    search_page.open()

    print(f"\n🧪 Запуск теста с параметрами: {test_case}")

    search_page.fill_form_f1(test_case)
    search_page.submit_f1()
    time.sleep(2)

    analyze_result_page(page, test_case, mode="f1")
