
@echo off
echo Starting test run with Allure reporting...

REM Run pytest with Allure results
pytest tests -s -v --alluredir=allure-results
if %ERRORLEVEL% NEQ 0 (
    echo Pytest failed. Check the output above.
    pause
    exit /b %ERRORLEVEL%
)

REM Generate Allure report
allure generate allure-results -o allure-report --clean
if %ERRORLEVEL% NEQ 0 (
    echo Allure report generation failed.
    pause
    exit /b %ERRORLEVEL%
)

REM Open Allure report
allure open allure-report
if %ERRORLEVEL% NEQ 0 (
    echo Failed to open Allure report.
    pause
    exit /b %ERRORLEVEL%
)

echo Test run and report generation completed successfully.
pause