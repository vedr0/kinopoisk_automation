import pytest
import allure
from playwright.sync_api import Page
pytestmark = pytest.mark.base

@allure.sub_suite("Полное название фильма")
@pytest.mark.parametrize("movie_name, expected_result", [
    ("Интерстеллар", "Интерстеллар"),
    ("Джентльмены", "Джентльмены"),
])
@allure.title("Поиск по полному названию: {movie_name}")
def test_search_movie_by_full_name(page: Page, movie_name: str, expected_result: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(movie_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    first_result = page.locator(".search_results .name a").first
    assert first_result.inner_text() == expected_result

@allure.sub_suite("Альтернативные названия")
@pytest.mark.parametrize("alt_name, expected_result", [
    ("Star Wars", "Звездные войны"),
    ("Avengers", "Мстители"),
])
@allure.title("Поиск по альтернативному названию: {alt_name}")
def test_search_by_alternative_name(page: Page, alt_name: str, expected_result: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(alt_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    results = page.locator(".search_results .name")
    found = any(alt_name in results.nth(i).inner_text() or expected_result in results.nth(i).inner_text() for i in range(results.count()))
    assert found

@allure.sub_suite("Проверка регистра")
@pytest.mark.parametrize("movie_name, expected_result", [
    ("ИнТеРсТеЛлАр", "Интерстеллар"),
    ("мСтИТеЛи", "Мстители"),
])
@allure.title("Поиск с нечувствительностью к регистру: {movie_name}")
def test_search_case_insensitive(page: Page, movie_name: str, expected_result: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(movie_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    first_result = page.locator(".search_results .name").first
    assert expected_result in first_result.inner_text()

@allure.sub_suite("Частичные совпадения")
@pytest.mark.parametrize("partial_name", [
    "Интер",
    "Star",
    "Ават",
])
@allure.title("Поиск по части названия: {partial_name}")
def test_partial_name_search(page: Page, partial_name: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(partial_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    results = page.locator(".search_results .name")
    found = any(partial_name.lower() in results.nth(i).inner_text().lower() for i in range(results.count()))
    assert found

@allure.sub_suite("Невалидные запросы")
@pytest.mark.parametrize("invalid_query, expected_message", [
    ("abcdefg", "К сожалению, по вашему запросу ничего не найдено..."),
    ("!!!@@@", "К сожалению, по вашему запросу ничего не найдено..."),
    ("a" * 100, "К сожалению, по вашему запросу ничего не найдено..."),
    ("'; DROP TABLE movies;--", "К сожалению, по вашему запросу ничего не найдено..."),
    ("<script>alert('XSS')</script>", "К сожалению, по вашему запросу ничего не найдено..."),
])
@allure.title("Невалидный запрос: {invalid_query}")
def test_invalid_search(page: Page, invalid_query: str, expected_message: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(invalid_query)
    search_input.press("Enter")
    no_results_message = page.locator("h2.textorangebig").first
    no_results_message.wait_for(state="visible")
    assert no_results_message.is_visible()
    assert expected_message in no_results_message.inner_text()

@allure.sub_suite("Пустой запрос")
@allure.title("Поиск с пустым запросом")
def test_empty_query(page: Page):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill("")
    search_input.press("Enter")
    page.wait_for_url("https://www.kinopoisk.ru/chance/", timeout=5000)
    assert "chance" in page.url
