import pytest
import allure
import csv
import time
from playwright.sync_api import Page, expect
from utils.page_analysis import analyze_result_page


@allure.step("Загрузка данных из CSV")
def load_test_data():
    test_data = []
    with open("test_data/f2_creator_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            test_data.append(row)
    return test_data

@pytest.mark.f2
@pytest.mark.parametrize("test_case", load_test_data())
@allure.title("Тест поиска по создателям/актерам (f2)")
@allure.description("Проверка формы поиска фильмов по создателям/актерам (режиссер, актер и т.д.) через f2")
def test_creator_search_f2(page: Page, test_case):
    page.goto("https://www.kinopoisk.ru/s/", wait_until="load")
    page.wait_for_selector("form[name='keyword_search']", timeout=20000)

    print(f"\n🔎 Запуск теста с параметрами: {test_case}")

    search_form = page.locator("form[name='keyword_search']")
    search_button = search_form.locator("#btn_search_6")

    @allure.step("Заполнение пары роль + имя")
    def fill_creator_pair(index: int, role: str, name: str):
        if role and role != "-":
            role_select = search_form.locator(f"#cr_search_field_{index}_select")
            expect(role_select).to_be_visible()
            role_select.select_option(role)
            print(f"✅ Роль {index}: {role}")

        if name and name.strip():
            name_input = search_form.locator(f"#cr_search_field_{index}")
            expect(name_input).to_be_visible()
            name_input.click()
            name_input.type(name, delay=100)

            # Проверка, не произошло ли редиректа сразу после ввода
            if not page.url.startswith("https://www.kinopoisk.ru/s/"):
                pytest.xfail(f"❌ Страница изменилась во время ввода '{name}' (role: {role}) — после type(): {page.url}")

            # ⏳ Ждём появления и отклика автокомплита (вручную, т.к. он не ловится по селекторам)
            time.sleep(2)
            page.keyboard.press("ArrowDown")
            time.sleep(2)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

            # Проверка после выбора из автокомплита
            if not page.url.startswith("https://www.kinopoisk.ru/s/"):
                pytest.xfail(f"❌ Страница изменилась после выбора из автокомплита '{name}' (role: {role}): {page.url}")

            name_input.evaluate("el => el.blur()")
            print(f"✅ Имя {index}: {name}")

    # 🔁 Перебор всех пар "Роль/Имя", заданных в CSV
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

        fill_creator_pair(index, role, name)
        index += 1

    # Активация кнопки поиска
    page.evaluate("CheckFields(6)")

    if not search_button.is_enabled():
        pytest.xfail("❌ Кнопка поиска не активна")

    search_button.click()
    page.wait_for_load_state("load")

    # Анализ результата поиска
    analyze_result_page(page, test_case, mode="f2")