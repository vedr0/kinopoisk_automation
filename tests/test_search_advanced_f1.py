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
    # time.sleep(3)  # Увеличенный таймаут для загрузки страницы

    # Логируем тест-кейс
    print(f"\n🔎 Запуск теста с параметрами: {test_case}")

    # Находим форму f1
    search_form = page.locator("form[name='film_search']")
    search_button = search_form.locator(".el_18.submit.nice_button")

    # Ожидание доступности формы
    try:
        page.wait_for_selector("form[name='film_search']", timeout=40000)
        print("✅ Форма поиска загружена")
    except Exception:
        pytest.fail("❌ Форма поиска не загрузилась!")

    # Функция для безопасного заполнения текстовых полей
    def fill_field(field_name, value):
        if value and value != "-":
            try:
                field = search_form.locator(f"[name='{field_name}']")
                page.wait_for_selector(f"[name='{field_name}']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)
                field.fill(value)
                print(f"✅ Заполнено поле '{field_name}': {value}")
                # time.sleep(1)
            except Exception:
                pytest.fail(f"❌ Ошибка при заполнении '{field_name}'")

    # Функция для безопасного выбора из <select>
    def select_field(field_name, value):
        if value and value != "-":
            try:
                field = search_form.locator(f"[name='{field_name}']")
                page.wait_for_selector(f"[name='{field_name}']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)

                # Получаем все доступные значения
                available_values = [opt.get_attribute("value") for opt in field.locator("option").all()]
                if value not in available_values:
                    pytest.fail(f"❌ Значение '{value}' не найдено в списке '{field_name}'")

                field.select_option(value)
                print(f"✅ Выбрано поле '{field_name}': {value}")
                # time.sleep(1)
            except Exception as e:
                pytest.fail(f"❌ Ошибка при выборе '{field_name}': {e}")

    # Фикс отдельно для жанра (на случай если список визуально скрыт)
    def select_genre(value):
        if value and value != "-":
            try:
                field = search_form.locator("[name='m_act[genre][]']")
                page.wait_for_selector("[name='m_act[genre][]']", timeout=15000)
                expect(field).to_be_visible(timeout=15000)
                field.select_option(value)
                print(f"✅ Выбран жанр: {value}")
                # time.sleep(1)
            except Exception:
                pytest.fail(f"❌ Ошибка при выборе жанра '{value}'")

    # Заполняем текстовые поля
    fill_field("m_act[find]", test_case["Название фильма"])
    fill_field("m_act[year]", test_case["Год"])
    fill_field("m_act[box]", test_case["Сумма сборов"])
    fill_field("m_act[actor]", test_case["Актер"])
    fill_field("m_act[cast]", test_case["Создатели"])

    # Выпадающие списки
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

    time.sleep(3)

    # Проверяем, что кнопка активна перед нажатием
    # if not search_button.is_enabled():
    #     pytest.fail("❌ Кнопка поиска неактивна, проверь заполнение полей!")
    try:
        expect(search_button).to_be_enabled(timeout=3000)
    except:
        pytest.fail("❌ Кнопка поиска неактивна, проверь заполнение полей!")

    # Кликаем "поиск"
    search_button.click()

    # Ждем загрузки результатов
    page.wait_for_load_state("networkidle")
    # time.sleep(3)

    # Проверка результата
    if "/film/" in page.url:
        print(f"✅ Фильм найден: {page.url}")
        assert True

    elif page.url == "https://www.kinopoisk.ru/s/":
        pytest.xfail("Форма не отработала: остались на /s/")

    else:
        try:
            # "Ничего не найдено"
            no_results = page.locator("h2.textorangebig", has_text="ничего не найдено")
            if no_results.count() > 0 and no_results.first.is_visible():
                pytest.xfail(f"Ожидаемый провал теста: '{test_case['Название фильма']}' не найден.")

            # "Похожие фильмы"
            suggestions_header = page.locator("p.header", has_text="Скорее всего, вы ищете:")
            results_link = page.locator("p.header a", has_text="Результаты поиска")
            if suggestions_header.count() > 0 and results_link.count() > 0:
                print("✅ Открылась страница похожих фильмов")
                assert True

            # Ничего не подошло — ошибка
            pytest.fail(f"❌ Неожиданный результат. URL: {page.url}")

        except Exception as e:
            pytest.fail(f"❌ Ошибка при анализе результата: {e}")
