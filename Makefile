.PHONY: test-all test-f1 test-f2 test-base all-report open-report clean

test-all:
	pytest -s -p pytest_playwright --browser=chromium --headed --alluredir=allure-results

test-f1:
	pytest -s -p pytest_playwright -m f1 --browser=chromium --headed --alluredir=allure-results

test-f2:
	pytest -s -p pytest_playwright -m f2 --browser=chromium --headed --alluredir=allure-results

test-base:
	pytest -s -p pytest_playwright tests/test_search_base.py --browser=chromium --headed --alluredir=allure-results

all-report:
	allure generate allure-results --clean -o allure-report

open-report:
	allure open allure-report

clean:
	rd /s /q allure-results allure-report || true