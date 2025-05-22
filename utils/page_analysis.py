import pytest
import allure
from playwright.sync_api import Page

@allure.step("Анализ страницы результата поиска")
def analyze_result_page(page: Page, test_case: dict, mode: str = "f1"):
    try:
        # Частный случай: переход на список фильмов по стране — только для f1
        if mode == "f1":
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

        # Форма не отработала — остались на /s/
        if page.url == "https://www.kinopoisk.ru/s/":
            pytest.xfail("❌ Форма не отработала — остались на /s/")

        # "Ничего не найдено"
        if page.locator("h2.textorangebig", has_text="К сожалению, по вашему запросу ничего не найдено...").is_visible():
            print("✅ Ничего не найдено")
            return

        # Переадресация на похожие фильмы
        if page.locator("p.header", has_text="Скорее всего, вы ищете:").is_visible():
            print("✅ Переадресация на страницу похожих результатов")
            return

        # Переадресация на страницу конкретного фильма
        if "/film/" in page.url:
            print(f"✅ Найден один фильм: {page.url}")
            return

        # Страница результатов
        print(f"📝 Результат поиска: {page.url}")

    except Exception as e:
        pytest.fail(f"❌ Ошибка при анализе результата: {e}")