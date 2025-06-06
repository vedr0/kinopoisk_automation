def get_sub_suite_f1(test_case: dict) -> str:
    def is_filled(val):
        return val and val.strip() and val.strip() != "-"

    filled_fields = {k for k, v in test_case.items() if is_filled(v)}

    # Обязательные поля — хотя бы одно из них должно быть для валидного запроса
    required_groups = [
        {"Название фильма"},
        {"Год"},
        {"Начало интервала годов", "Конец интервала годов"},
        {"Страна"},
        {"Жанр"},
        {"Прокатчик"},
        {"Месяц премьеры", "Год премьеры", "Страна премьеры"},
    ]

    # Если ни одна из обязательных групп не заполнена — считаем как "Пустой тест-кейс"
    def has_required():
        for group in required_groups:
            if group <= filled_fields or group & filled_fields == group:
                return True
        return False

    # Кейсы с заполнением одного поля
    if filled_fields == {"Название фильма"}:
        return "Поле: Название фильма - m_act[find]"
    if filled_fields == {"Год"}:
        return "Поле: Год - m_act[year]"
    if filled_fields == {"Начало интервала годов", "Конец интервала годов"}:
        return "Поле: Интервал годов - m_act[from_year], m_act[to_year]"
    if filled_fields == {"Страна"}:
        return "Поле: Страна - m_act[country]"
    if filled_fields == {"Жанр"}:
        return "Поле: Жанр - m_act[genre]"
    if filled_fields == {"Прокатчик"}:
        return "Поле: Прокатчик - m_act[company]"
    if filled_fields == {"Месяц премьеры", "Год премьеры", "Страна премьеры"}:
        return "Поле: Премьера - m_act[premier_month], m_act[premier_year], m_act[premier_type]"

    # Если заполнены только необязательные поля
    optional_fields = {
        "Сравнение сборов", "Сумма сборов", "Страна сборов",
        "Что искать?", "Актер", "Создатели", "MPAA рейтинг"
    }
    if filled_fields <= optional_fields:
        return "Пустой тест-кейс"

    return "Комбинированные/Сложные сценарии"