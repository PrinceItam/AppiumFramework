# AppiumFramework

![Appium](https://img.shields.io/badge/Appium-2.5.1-blue.svg)
![pytest](https://img.shields.io/badge/pytest-7.4.0-green.svg)
![Allure](https://img.shields.io/badge/Allure-2.29.0-orange.svg)
![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)

A robust automated testing framework for Android applications using **Appium**, **pytest**, and **Allure reporting**. This project provides a structured setup for testing mobile apps, with reusable page objects, custom assertions, and detailed test reports.

## Features
- **Appium Integration:** Automates Android app testing with Appium’s WebDriver.
- **pytest Framework:** Organized test cases with fixtures and parameterization.
- **Allure Reporting:** Beautiful, detailed test reports with screenshots on failure.
- **Page Object Model:** Maintainable and scalable test design.
- **Custom Utilities:** Logging, assertions, and driver management.
- **Docker Support:** Containerized test execution for consistency.

## Prerequisites
- **Python 3.9+**: Install from [python.org](https://www.python.org).
- **Appium Server**: Install via npm: `npm install -g appium`.
- **Android SDK**: Set up with an emulator (e.g., Pixel_8_Pro_API_Baklava).
- **Git**: To clone this repository.
- **Docker** (optional): For containerized runs.

## Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/PrinceItam/AppiumFramework.git
   cd AppiumFramework

python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

pip install -r requirements.txt

## Run test in windows cmd or Mac .sh 
./Run_test.sh
./Run_test.cm

## Docker Execution
docker run --rm -v "$PWD/allure-report:/app/allure-report" appium-tests

### View report 
allure open allure-report
