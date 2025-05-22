### README.md

# Kinopoisk Automation Testing

Автоматизация тестирования сайта [kinopoisk.ru](https://www.kinopoisk.ru) с использованием Playwright + Pytest + Allure.

## Структура проекта

```
kinopoisk_automation/
├── tests/
│ ├── test_search_advanced_f1.py      # тесты формы f1 «Искать фильм»
│ ├── test_search_by_creator_f2.py    # тесты формы f2 «Искать по создателям»
│ └── test_search_base.py             # базовый поиск по названию
├── utils/
│ ├── page_analysis.py                # общий анализ результата поиска
│ └── form_interaction.py             # заполнение полей форм f1 и f2
├── page_objects/
│ └── advanced_search_page.py         # Page Object для форм f1 и f2
├── test_data/
│ ├── f1_advanced_search_test_data.csv
│ └── f2_creator_search_test_data.csv
├── requirements.txt
├── README.md
└── pytest.ini
```

## Команды запуска

### Установка зависимостей:
```
pip install -r requirements.txt
playwright install
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

## Дополнительно
- Все нестабильные/ожидаемо проваливающиеся кейсы отмечены через `pytest.xfail()`
- Данные загружаются из CSV (за исключением test_search_base)

---

### requirements.txt

```
playwright>=1.43.0
pytest>=8.0.0
allure-pytest>=2.13.5
