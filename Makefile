.PHONY: test-f1 test-f2 test-base all-report clean open-report

test-f1:
	pytest -m f1 --headed --alluredir=allure-results

test-f2:
	pytest -m f2 --headed --alluredir=allure-results

test-base:
	pytest tests/test_search_base.py --headed --alluredir=allure-results

all-report:
	allure generate allure-results --clean -o allure-report

open-report:
	start allure-report/index.html

clean:
	rd /s /q allure-results allure-report