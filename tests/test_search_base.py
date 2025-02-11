import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("movie_name, expected_result", [
    ("Интерстеллар", "Интерстеллар"),
    ("Джентльмены", "Джентльмены"),
])
def test_search_movie_by_full_name(page: Page, movie_name: str, expected_result: str):
    """
    Тест: Поиск фильма по полному названию.
    Шаги:
    1. Ввести название фильма в поле поиска.
    2. Нажать Enter.
    Ожидание:
    - На странице отображается список результатов.
    - Первый результат соответствует запросу.
    """
    page.goto("https://www.kinopoisk.ru/")
    # Находим поле поиска и вводим название фильма
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(movie_name)
    search_input.press("Enter")
    # Ожидаем загрузку страницы с результатами поиска
    page.wait_for_selector(".search_results")
    # Проверяем, что первый результат соответствует запросу
    first_result = page.locator(".search_results .name a").first
    assert first_result.inner_text() == expected_result, (
        f"Ожидалось: {expected_result}, но найдено: {first_result.inner_text()}"
    )

@pytest.mark.parametrize("alt_name, expected_result", [
    ("Star Wars", "Звездные войны"),  # Пример с альтернативным названием
    ("Avengers", "Мстители"),
])
def test_search_by_alternative_name(page: Page, alt_name: str, expected_result: str):
    """
    Тест: Поиск фильма по альтернативному названию.
    Шаги:
    1. Ввести альтернативное название фильма/сериала в поле поиска.
    2. Нажать Enter.
    Ожидание:
    - Найден фильм по альтернативному названию.
    """
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(alt_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    # Проверяем, что alt_name или expected_result присутствует в любом элементе
    results = page.locator(".search_results .name")
    found = False
    for i in range(results.count()):
        if alt_name in results.nth(i).inner_text() or expected_result in results.nth(i).inner_text():
            found = True
            break

    assert found, f"'{alt_name}' или '{expected_result}' не найдены в результатах поиска."

@pytest.mark.parametrize("movie_name, expected_result", [
    ("ИнТеРсТеЛлАр", "Интерстеллар"),
    ("мСтИТеЛи", "Мстители"),
])
def test_search_case_insensitive(page: Page, movie_name: str, expected_result: str):
    """
    Тест: Поиск фильма с учетом регистра.
    Шаги:
    1. Ввести название в произвольном регистре.
    2. Нажать Enter.
    Ожидание:
    - Найден фильм по корректному названию.
    """
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(movie_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    first_result = page.locator(".search_results .name").first
    assert expected_result in first_result.inner_text(), (
        f"Ожидалось: {expected_result}, но найдено: {first_result.inner_text()}"
    )

@pytest.mark.parametrize("partial_name", [
    "Интер",
    "Star",
    "Ават",
])
def test_partial_name_search(page: Page, partial_name: str):
    # Ввод частичного названия
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(partial_name)
    search_input.press("Enter")
    page.wait_for_selector(".search_results")
    # Проверяем, что хотя бы один из результатов содержит partial_name
    results = page.locator(".search_results .name")
    found = False
    for i in range(results.count()):
        if partial_name.lower() in results.nth(i).inner_text().lower():
            found = True
            break

    assert found, f"'{partial_name}' не найдено в результатах поиска"

@pytest.mark.parametrize("invalid_query, expected_message", [
    ("abcdefg", "К сожалению, по вашему запросу ничего не найдено..."),  # Несуществующее название
    ("!!!@@@", "К сожалению, по вашему запросу ничего не найдено..."),  # Специальные символы
    ("a" * 100, "К сожалению, по вашему запросу ничего не найдено..."),  # Длинный запрос
    ("'; DROP TABLE movies;--", "К сожалению, по вашему запросу ничего не найдено..."),  # SQL-инъекция
    ("<script>alert('XSS')</script>", "К сожалению, по вашему запросу ничего не найдено...")  # XSS
])

def test_invalid_search(page: Page, invalid_query: str, expected_message: str):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill(invalid_query)
    search_input.press("Enter")
    no_results_message = page.locator("h2.textorangebig").first
    no_results_message.wait_for(state="visible")

    assert no_results_message.is_visible(), "Сообщение о том, что ничего не найдено, не отображается."
    assert expected_message in no_results_message.inner_text(), f"Ожидалось сообщение '{expected_message}', но получено '{no_results_message.inner_text()}'"


def test_empty_query(page: Page):
    page.goto("https://www.kinopoisk.ru/")
    search_input = page.locator('[name="kp_query"]')
    search_input.fill("")
    search_input.press("Enter")
    page.wait_for_url("https://www.kinopoisk.ru/chance/", timeout=5000)

    assert "chance" in page.url, f"Ожидался переход на /chance/, но открыта страница {page.url}"