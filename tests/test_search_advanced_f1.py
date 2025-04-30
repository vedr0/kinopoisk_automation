import pytest
from playwright.sync_api import Page, expect
import csv
import time


# Читаем тестовые данные из CSV-файла
def load_test_data():
    test_data = []
    with open("test_data/f1_advanced_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            test_data.append(row)
    return test_data


@pytest.mark.parametrize("test_case", load_test_data())
def test_advanced_search_f1(page: Page, test_case):
    page.goto("https://www.kinopoisk.ru/s/", wait_until="load")
    page.wait_for_selector("form[name='film_search']", timeout=30000)

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
                    pytest.xfail(f"Недопустимое значение '{value}' для поля '{field_name}'")
                field.select_option(value)
                print(f"✅ Выбрано поле '{field_name}': {value}")
            except Exception as e:
                pytest.fail(f"❌ Ошибка при выборе '{field_name}': {e}")

    def select_genres(page: Page, values: list[str]):
        select = page.locator("select[name='m_act[genre][]']")
        page.wait_for_selector("select[name='m_act[genre][]']", timeout=15000)
        expect(select).to_be_visible(timeout=15000)

        # Получаем допустимые значения
        available_values = select.locator("option").evaluate_all("opts => opts.map(o => o.value)")
        valid_values = [v for v in values if v in available_values]

        if not valid_values:
            pytest.xfail(f"Ни один из жанров {values} не валиден — форма не активируется")

        select.evaluate("el => Array.from(el.options).forEach(o => o.selected = false)")
        select.select_option(valid_values)
        print(f"✅ Выбраны жанры: {valid_values}")

    def analyze_result_page(page: Page, test_case: dict):
        try:
            # 🔍 Обработка случая, когда указана только страна
            country_value = test_case.get("Страна", "").strip()
            has_only_country = (
                    country_value and country_value != "-"
                    and all(
                v.strip() in ("", "-")
                for k, v in test_case.items()
                if k != "Страна"
            )
            )
            if has_only_country:
                expected_url_part = f"/lists/m_act[country]/{country_value}/"
                if expected_url_part in page.url:
                    print(f"✅ Перешли на страницу фильмов по стране: {page.url}")
                    return
                else:
                    pytest.xfail(f"❌ Ожидался редирект на {expected_url_part}, но URL: {page.url}")

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
            if header_similar.is_visible():
                print("✅ Открылась страница похожих фильмов")
                return

            # Если ни один из паттернов не сработал — отладочный вывод
            print("🔍 Отладка: p.header видим?", header_similar.is_visible())
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
    # Жанры: мультивыбор через CTRL
    raw_genre = test_case.get("Жанр", "").strip()
    genre_values = [v.strip() for v in raw_genre.split(",") if v.strip() and v != "-"]
    if genre_values:
        select_genres(page, genre_values)
    select_field("m_act[company]", test_case["Прокатчик"])
    select_field("m_act[mpaa]", test_case["MPAA рейтинг"])
    select_field("m_act[premier_month]", test_case["Месяц премьеры"])
    select_field("m_act[premier_year]", test_case["Год премьеры"])
    select_field("m_act[premier_type]", test_case["Регион премьеры"])
    select_field("m_act[box_vector]", test_case["Сравнение сборов"])
    select_field("m_act[box_type]", test_case["Регион сборов"])
    select_field("m_act[content_find]", test_case["Что искать?"])

    if not search_button.is_enabled():
        notice_block = page.locator("#ui_notice_container .tdtext", has_text="уменьшите количество лет")
        if notice_block.is_visible():
            pytest.xfail("❌ Появилось предупреждение об ограничении интервала (макс. 10 лет)")
        else:
            pytest.xfail("❌ Кнопка поиска неактивна, вероятно из-за некорректного заполнения формы")

    # Если кнопка активна — кликаем и продолжаем
    search_button.click()
    page.wait_for_load_state("load")
    if page.url == "https://www.kinopoisk.ru/s/":
        pytest.xfail("Форма не отработала: остались на /s/")
    time.sleep(3)

    analyze_result_page(page, test_case)
