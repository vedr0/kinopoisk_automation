import pytest
from playwright.sync_api import Page, Locator, expect
import allure
import logging


logger = logging.getLogger(__name__)
def get_search_form(page: Page, mode: str) -> Locator:
    if mode == "f1":
        return page.locator("form[name='film_search']")
    elif mode == "f2":
        return page.locator("form[name='keyword_search']")
    else:
        raise ValueError(f"Неизвестный mode: {mode}")


@allure.step("Заполнение текстового поля: {field_name} = {value}")
def fill_field(page: Page, mode: str, field_name: str, value: str):
    if value and value != "-":
        try:
            form = get_search_form(page, mode)
            field = form.locator(f"[name='{field_name}']")
            expect(field).to_be_visible(timeout=15000)

            if field_name in ["m_act[find]", "m_act[year]"]:
                field.click()
                field.type(value, delay=100)
                field.evaluate("el => el.blur()")
            else:
                field.fill(value)

            logger.info(f"📝 Заполнено поле '{field_name}': {value}")
        except Exception:
            pytest.fail(f"❌ Ошибка при заполнении '{field_name}'")


@allure.step("Выбор значения из списка: {field_name} = {value}")
def select_field(page: Page, mode: str, field_name: str, value: str):
    if value and value != "-":
        try:
            form = get_search_form(page, mode)
            field = form.locator(f"[name='{field_name}']")
            expect(field).to_be_visible(timeout=15000)
            available_values = [opt.get_attribute("value") for opt in field.locator("option").all()]
            if value not in available_values:
                pytest.xfail(f"❌ Недопустимое значение '{value}' для поля '{field_name}'")
            field.select_option(value)
            logger.info(f"📝 Выбрано поле '{field_name}': {value}")
        except Exception as e:
            pytest.fail(f"❌ Ошибка при выборе '{field_name}': {e}")


@allure.step("Выбор жанров: {values}")
def select_genres(page: Page, mode: str, values: list[str]):
    form = get_search_form(page, mode)
    select = form.locator("select[name='m_act[genre][]']")
    expect(select).to_be_visible(timeout=15000)
    available_values = select.locator("option").evaluate_all("opts => opts.map(o => o.value)")
    valid_values = [v for v in values if v in available_values]

    if not valid_values:
        pytest.xfail(f"❌ Ни один из жанров {values} не валиден — форма не активируется")

    select.evaluate("el => Array.from(el.options).forEach(o => o.selected = false)")
    select.select_option(valid_values)

    logger.info(f"📝 Выбраны жанры: {valid_values}")


@allure.step("Заполнение пары Роль + Имя в f2")
def fill_creator_pair(page: Page, index: int, role: str, name: str):
    if role and role != "-":
        role_select = page.locator(f"#cr_search_field_{index}_select")
        page.wait_for_selector(f"#cr_search_field_{index}_select", timeout=10000)
        expect(role_select).to_be_visible()
        available_roles = [opt.get_attribute("value") for opt in role_select.locator("option").all()]
        if role not in available_roles:
            pytest.xfail(f"❌ Недопустимое значение '{role}' для поля 'Роль {index}'")
        role_select.select_option(role)

        logger.info(f"📝 Роль {index}: {role}")

    if name and name.strip():
        name_input = page.locator(f"#cr_search_field_{index}")
        expect(name_input).to_be_visible()
        name_input.click()
        name_input.type(name, delay=100)
        page.wait_for_timeout(1000)
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(1000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        name_input.evaluate("el => el.blur()")

        logger.info(f"📝 Имя {index}: {name}")
