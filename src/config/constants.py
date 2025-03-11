import os

# Directory settings
SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")
LOG_DIR = os.getenv("LOG_DIR", "logs")
ALLURE_DIR = os.getenv("ALLURE_DIR", "allure-results")
TEST_RESOURCES_DIR = os.getenv("TEST_RESOURCES_DIR", "tests/resources")

# Appium settings
APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")  # Use localhost
APPIUM_PORT = os.getenv("APPIUM_PORT", "4723")
APK_PATH = os.getenv("APK_PATH", os.path.join(TEST_RESOURCES_DIR, "Android_Demo_App.apk"))
APP_PACKAGE = "com.code2lead.kwad"
APP_ACTIVITY = "com.code2lead.kwad.MainActivity"