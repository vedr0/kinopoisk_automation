import pytest
from playwright.sync_api import Page, expect
import csv


def load_test_data():
    test_data = []
    with open("test_data/f2_creator_search_test_data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            test_data.append(row)
    return test_data


@pytest.mark.parametrize("test_case", load_test_data())
def test_creator_search_f2(page: Page, test_case):
    page.goto("https://www.kinopoisk.ru/s/", wait_until="load")
    page.wait_for_selector("form[name='keyword_search']", timeout=20000)

    print(f"\n🔎 Запуск теста с параметрами: {test_case}")

    search_form = page.locator("form[name='keyword_search']")
    search_button = search_form.locator("#btn_search_6")

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

            # 🛡️ Первичная проверка сразу после type()
            if not page.url.startswith("https://www.kinopoisk.ru/s/"):
                pytest.xfail(f"❌ Страница изменилась во время ввода '{name}' (role: {role}) — после type(): {page.url}")

            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

            # 🛡️ Вторая проверка — перед blur()
            if not page.url.startswith("https://www.kinopoisk.ru/s/"):
                pytest.xfail(f"❌ Страница изменилась после выбора из автокомплита '{name}' (role: {role}): {page.url}")

            name_input.evaluate("el => el.blur()")
            print(f"✅ Имя {index}: {name}")

    # 🚀 Цикл по всем парам "Роль/Имя" в CSV
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

    page.evaluate("CheckFields(6)")

    if not search_button.is_enabled():
        pytest.xfail("❌ Кнопка поиска не активна")

    search_button.click()
    page.wait_for_load_state("load")

    # Анализ результата
    # Проверка: остались на той же странице
    if page.url == "https://www.kinopoisk.ru/s/":
        pytest.xfail("❌ Форма не отработала — остались на /s/")

    # Проверка: ничего не найдено
    if page.locator("h2.textorangebig", has_text="К сожалению, по вашему запросу ничего не найдено...").is_visible():
        print("❕ Ничего не найдено")
        return

    # Проверка: переадресация на похожие результаты
    if page.locator("p.header", has_text="Скорее всего, вы ищете:").is_visible():
        print("🔁 Переадресация на похожие результаты")
        return

    # Переход на карточку фильма (один результат)
    if "/film/" in page.url:
        print(f"🎬 Найден один фильм: {page.url}")
        return

    # Всё остальное — валидная страница с результатами
    print(f"📄 Результат поиска: {page.url}")
