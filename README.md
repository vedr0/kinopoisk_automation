# Kinopoisk Automation Testing

Автоматизация тестирования сайта [kinopoisk.ru](https://www.kinopoisk.ru) с использованием Playwright + Pytest + Allure.

## Структура проекта

```
kinopoisk_automation/
├── tests/
│ ├── test_search_advanced_f1.py # тесты формы f1 «Искать фильм»
│ ├── test_search_by_creator_f2.py # тесты формы f2 «Искать по создателям»
│ └── test_search_base.py # базовый поиск по названию
├── utils/
│ ├── form_interaction.py # функции заполнения форм f1 и f2
│ ├── page_analysis.py # логика анализа результата поиска
│ └── suite_utils.py # определение категории тестов для Allure SubSuite
├── page_objects/
│ ├── base_page.py # базовая логика поиска
│ └── advanced_search_page.py # Page Object для форм f1 и f2
├── test_data/
│ ├── f1_advanced_search_test_data.csv
│ └── f2_creator_search_test_data.csv
├── run_tests.bat # CLI-меню запуска тестов и генерации отчёта
├── Makefile # для кроссплатформенного тестирования
├── requirements.txt
├── pytest.ini
└── README.md
```

## Команды запуска

### Установка зависимостей:
```
pip install -r requirements.txt
playwright install
```
### Запуск через CLI-меню
```
Файл `run_tests.bat` позволяет выбрать браузер и запустить:
- все тесты сразу;
- тесты форм f1, f2 или base отдельно;
- генерацию и просмотр Allure-отчёта;
- очистку папок `allure-results` и `allure-report`.
```

### Запуск всех тестов:
```
pytest --headed --alluredir=allure-results
```

### Запуск конкретных тестов:
```
pytest tests/test_search_advanced_f1.py --headed --alluredir=allure-results
pytest tests/test_search_by_creator_f2.py --headed --alluredir=allure-results
pytest tests/test_search_base.py --headed --alluredir=allure-results

pytest -m f1 --headed --alluredir=allure-results   # запуск тестов формы расширенного поиска f1
pytest -m f2 --headed --alluredir=allure-results   # запуск тестов формы расширенного поиска f2
pytest -m \"f1 or f2\" --headed --alluredir=allure-results  # все тесты форм
pytest -m \"not f2\" --headed --alluredir=allure-results  # без f2

```

### Маркировка тестов:
- `@pytest.mark.f1` — тесты формы f1
- `@pytest.mark.f2` — тесты формы f2
- `pytestmark = pytest.mark.base` — тесты общего поиска

### Генерация и просмотр Allure-отчёта:
```
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## requirements.txt
```
playwright>=1.43.0
pytest>=8.0.0
allure-pytest>=2.13.5
pytest-playwright>=0.6.2
```