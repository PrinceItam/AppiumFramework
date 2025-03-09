#!/bin/bash

echo "Starting test run with Allure reporting..."

# Run pytest with Allure results
pytest tests -s -v --alluredir=allure-results
if [ $? -ne 0 ]; then
    echo "Pytest failed. Check the output above."
    exit 1
fi

# Generate Allure report
allure generate allure-results -o allure-report --clean
if [ $? -ne 0 ]; then
    echo "Allure report generation failed."
    exit 1
fi

# Open Allure report
allure open allure-report
if [ $? -ne 0 ]; then
    echo "Failed to open Allure report."
    exit 1
fi

echo "Test run and report generation completed successfully."