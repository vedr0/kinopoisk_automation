import pytest
import allure
import csv
import time
from playwright.sync_api import Page
from utils.page_analysis import analyze_result_page
from utils.form_interaction import fill_field, select_field, select_genres


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
    page.goto("https://www.kinopoisk.ru/s/", wait_until="load")
    page.wait_for_selector("form[name='film_search']", timeout=30000)
    print(f"\n🔎 Запуск теста с параметрами: {test_case}")

    fill_field(page, "f1", "m_act[find]", test_case["Название фильма"])
    fill_field(page, "f1", "m_act[year]", test_case["Год"])
    fill_field(page, "f1", "m_act[box]", test_case["Сумма сборов"])
    fill_field(page, "f1", "m_act[actor]", test_case["Актер"])
    fill_field(page, "f1", "m_act[cast]", test_case["Создатели"])

    select_field(page, "f1", "m_act[from_year]", test_case["Начало интервала годов"])
    select_field(page, "f1", "m_act[to_year]", test_case["Конец интервала годов"])
    select_field(page, "f1", "m_act[country]", test_case["Страна"])

    raw_genre = test_case.get("Жанр", "").strip()
    genre_values = [v.strip() for v in raw_genre.split(",") if v.strip() and v != "-"]
    if genre_values:
        select_genres(page, "f1", genre_values)

    select_field(page, "f1", "m_act[company]", test_case["Прокатчик"])
    select_field(page, "f1", "m_act[mpaa]", test_case["MPAA рейтинг"])
    select_field(page, "f1", "m_act[premier_month]", test_case["Месяц премьеры"])
    select_field(page, "f1", "m_act[premier_year]", test_case["Год премьеры"])
    select_field(page, "f1", "m_act[premier_type]", test_case["Регион премьеры"])
    select_field(page, "f1", "m_act[box_vector]", test_case["Сравнение сборов"])
    select_field(page, "f1", "m_act[box_type]", test_case["Регион сборов"])
    select_field(page, "f1", "m_act[content_find]", test_case["Что искать?"])

    search_button = page.locator("form[name='film_search'] .el_18.submit.nice_button")
    if not search_button.is_enabled():
        notice_block = page.locator("#ui_notice_container .tdtext", has_text="уменьшите количество лет")
        if notice_block.is_visible():
            pytest.xfail("❌ Появилось предупреждение об ограничении интервала (макс. 10 лет)")
        else:
            pytest.xfail("❌ Кнопка поиска неактивна, вероятно из-за некорректного заполнения формы")

    search_button.click()
    page.wait_for_load_state("load")
    if page.url == "https://www.kinopoisk.ru/s/":
        pytest.xfail("Форма не отработала: остались на /s/")
    time.sleep(3)

    analyze_result_page(page, test_case, mode="f1")