# """
# Тесты расширенного поиска
# """
#
# from page_objects.search_page import SearchPage
#
# def test_advanced_search(page):
#     search_page = SearchPage(page)
#     search_page.page.goto("https://www.kinopoisk.ru/s/")
#     search_page.set_year_filter("2000", "2010")
#     search_page.select_genre("комедия")
#     search_page.perform_search("")
#
#     assert "2000-2010" in search_page.page.inner_text(".search_results"), "Фильтры по году не сработали!"
#     assert "комедия" in search_page.page.inner_text(".search_results"), "Фильтры по жанру не сработали!"
