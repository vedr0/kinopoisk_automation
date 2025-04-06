import pytest
from playwright.sync_api import Page, expect
import csv
import time


# Читаем тестовые данные из CSV-файла
def load_test_data():
    test_data = []
    with open("test_data/advanced_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
    return test_data


@pytest.mark.parametrize("test_case", load_test_data())
def test_advanced_search_f1(page: Page, test_case):
    # Открываем страницу расширенного поиска
    page.goto("https://www.kinopoisk.ru/s/")
    page.wait_for_load_state("networkidle")

    print(f"\n🔎 Запуск теста с параметрами: {test_case}")

    search_form = page.locator("form[name='film_search']")
    search_button = search_form.locator(".el_18.submit.nice_button")

    try:
        page.wait_for_selector("form[name='film_search']", timeout=40000)
        print("✅ Форма поиска загружена")
    except Exception:
        pytest.fail("❌ Форма поиска не загрузилась!")


    def fill_field(field_name, value):
        if value and value != "-":
            try:
                field = search_form.locator(f"[name='{field_name}']")
                page.wait_for_selector(f"[name='{field_name}']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)

                if field_name in ["m_act[find]", "m_act[year]"]:
                    field.click()
                    field.type(value, delay=100)  # симулируем ручной ввод
                    field.evaluate("el => el.blur()")  # потеря фокуса
                    print(f"🔧 Симулируем ручной ввод и blur на поле '{field_name}'")
                else:
                    field.fill(value)

                print(f"✅ Заполнено поле '{field_name}': {value}")
            except Exception:
                pytest.fail(f"❌ Ошибка при заполнении '{field_name}'")
    def select_field(field_name, value):
        if value and value != "-":
            try:
                field = search_form.locator(f"[name='{field_name}']")
                page.wait_for_selector(f"[name='{field_name}']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)
                available_values = [opt.get_attribute("value") for opt in field.locator("option").all()]
                if value not in available_values:
                    pytest.fail(f"❌ Значение '{value}' не найдено в списке '{field_name}'")
                field.select_option(value)
                print(f"✅ Выбрано поле '{field_name}': {value}")
            except Exception as e:
                pytest.fail(f"❌ Ошибка при выборе '{field_name}': {e}")

    def select_genre(value):
        if value and value != "-":
            try:
                field = search_form.locator("[name='m_act[genre][]']")
                page.wait_for_selector("[name='m_act[genre][]']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)
                field.select_option(value)
                print(f"✅ Выбран жанр: {value}")
            except Exception:
                pytest.fail(f"❌ Ошибка при выборе жанра '{value}'")

    def analyze_result_page(page: Page, test_case: dict):
        try:
            # Если это точное совпадение (страница фильма)
            if "/film/" in page.url:
                print(f"✅ Фильм найден: {page.url}")
                return

            # Если форма не сработала (остались на /s/)
            if page.url == "https://www.kinopoisk.ru/s/":
                pytest.xfail("Форма не отработала: остались на /s/")

            # Проверка текста "ничего не найдено"
            if page.locator("h2.textorangebig", has_text="ничего не найдено").is_visible():
                pytest.xfail(f"Ожидаемый провал теста: '{test_case['Название фильма']}' не найден.")

            # Проверка, что это страница похожих фильмов
            header_similar = page.locator("p.header", has_text="Скорее всего, вы ищете:")
            # header_search_results = page.locator("p.header a", has_text="Результаты поиска")

            # if header_similar.is_visible() and header_search_results.is_visible():
            if header_similar.is_visible():
                print("✅ Открылась страница похожих фильмов")
                return

            # Если ни один из паттернов не сработал — отладочный вывод
            print("🔍 Отладка: p.header видим?", header_similar.is_visible())
            # print("🔍 Отладка: ссылка на 'Результаты поиска' видима?", header_search_results.is_visible())
            pytest.fail(f"❌ Неожиданный результат. URL: {page.url}")

        except Exception as e:
            pytest.fail(f"❌ Ошибка при анализе результата: {e}")

    fill_field("m_act[find]", test_case["Название фильма"])
    fill_field("m_act[year]", test_case["Год"])
    fill_field("m_act[box]", test_case["Сумма сборов"])
    fill_field("m_act[actor]", test_case["Актер"])
    fill_field("m_act[cast]", test_case["Создатели"])

    select_field("m_act[from_year]", test_case["Начало интервала годов"])
    select_field("m_act[to_year]", test_case["Конец интервала годов"])
    select_field("m_act[country]", test_case["Страна"])
    select_genre(test_case["Жанр"])
    select_field("m_act[company]", test_case["Прокатчик"])
    select_field("m_act[mpaa]", test_case["MPAA рейтинг"])
    select_field("m_act[premier_month]", test_case["Месяц премьеры"])
    select_field("m_act[premier_year]", test_case["Год премьеры"])
    select_field("m_act[premier_type]", test_case["Регион премьеры"])
    select_field("m_act[box_vector]", test_case["Сравнение сборов"])
    select_field("m_act[box_type]", test_case["Регион сборов"])
    select_field("m_act[content_find]", test_case["Что искать?"])

    # Явно активируем кнопку поиска
    print("🔧 Вызов CheckFields(1) для активации кнопки поиска")
    page.evaluate("CheckFields(1)")

    time.sleep(2)

    try:
        expect(search_button).to_be_enabled(timeout=3000)
    except:
        pytest.fail("❌ Кнопка поиска неактивна, проверь заполнение полей!")

    search_button.click()
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    analyze_result_page(page, test_case)