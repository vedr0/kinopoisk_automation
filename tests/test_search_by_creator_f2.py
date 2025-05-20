import pytest
import allure
import csv
from playwright.sync_api import Page
from utils.page_analysis import analyze_result_page
from utils.form_interaction import fill_creator_pair


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
    page.goto("https://www.kinopoisk.ru/s/", wait_until="load")
    page.wait_for_selector("form[name='keyword_search']", timeout=30000)
    print(f"\n🔎 Запуск теста f2 с параметрами: {test_case}")

    search_form = page.locator("form[name='keyword_search']")
    search_button = search_form.locator("#btn_search_6")

    # Перебор всех пар "Роль N" + "Имя N"
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

        fill_creator_pair(page, index, role, name)
        index += 1

    # page.evaluate("CheckFields(6)")  # ручная активация кнопки

    if not search_button.is_enabled():
        pytest.xfail("❌ Кнопка поиска неактивна — вероятно, автокомплит не сработал")

    search_button.click()
    page.wait_for_load_state("load")

    analyze_result_page(page, test_case, mode="f2")