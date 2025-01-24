import pytest
from playwright.sync_api import sync_playwright

def test_authorized_access(context_with_auth):
    page = context_with_auth.new_page()  # Создаём новую страницу в контексте с авторизацией
    page.goto("https://www.kinopoisk.ru/")  # Переходим на сайт
    assert page.title() == "Кинопоиск. Онлайн кинотеатр. Фильмы сериалы мультфильмы и энциклопедия"  # Проверяем что заголовок страницы верный
