@echo off
setlocal enabledelayedexpansion
call venv\Scripts\activate.bat

:: 1. Выбор браузера
:choose_browser
cls
echo === Choose browser ===
echo 1. Chromium
echo 2. Firefox
echo 3. WebKit
set /p browser_choice=Input option number (1-3):

if "%browser_choice%"=="1" set BROWSER=chromium
if "%browser_choice%"=="2" set BROWSER=firefox
if "%browser_choice%"=="3" set BROWSER=webkit

echo Selected browser: !BROWSER!
pause

:: 2–6. Главное меню
:main_menu
cls
echo === Choose tests to run ===
echo 1. Run ALL tests
echo 2. Run f1 search tests
echo 3. Run f2 search tests
echo 4. Run base search tests
echo 5. Generate Allure-report
echo 6. Open Allure-report
echo 7. Delete Allure-report
echo 8. Quit

set /p choice=Chose option number (1-7):

if "%choice%"=="1" (
    pytest -p pytest_playwright --browser !BROWSER! --headed --alluredir=allure-results
    pause
)
if "%choice%"=="2" (
    pytest -p pytest_playwright -m f1 --browser !BROWSER! --headed --alluredir=allure-results
    pause
)
if "%choice%"=="3" (
    pytest -p pytest_playwright -m f2 --browser !BROWSER! --headed --alluredir=allure-results
    pause
)
if "%choice%"=="4" (
    pytest -p pytest_playwright tests/test_search_base.py --browser !BROWSER! --headed --alluredir=allure-results
    pause
)
if "%choice%"=="5" (
    allure generate allure-results --clean -o allure-report
    echo Allure-report generated
    pause
)
if "%choice%"=="6" (
    allure open allure-report
    pause
)
if "%choice%"=="7" (
    rmdir /s /q allure-results
    rmdir /s /q allure-report
    echo Allure-report, Allure-results deleted
    pause
)
if "%choice%"=="8" exit

goto main_menu