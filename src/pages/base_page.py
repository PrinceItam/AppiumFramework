from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from src.utilities.custom_logger import CustomLogger  # Adjusted path
from src.config.constants import SCREENSHOT_DIR  # Adjusted path
import os
from datetime import datetime

logger = CustomLogger.get_logger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator_value, locator_type, timeout=10, poll_frequency=0.5):
        """Wait for an element to be present in the DOM and visible."""
        try:
            locator_map = {
                "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
                "id": AppiumBy.ID,
                "xpath": AppiumBy.XPATH,
                "class_name": AppiumBy.CLASS_NAME,
                "text": AppiumBy.ANDROID_UIAUTOMATOR,
                "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
                "uiautomator_text": AppiumBy.ANDROID_UIAUTOMATOR,
                "uiautomator_desc": AppiumBy.ANDROID_UIAUTOMATOR,
                "uiautomator_class": AppiumBy.ANDROID_UIAUTOMATOR
            }
            if locator_type not in locator_map:
                raise ValueError(f"Invalid locator_type: {locator_type}")

            if locator_type in ["text", "uiautomator_text", "uiautomator_desc", "uiautomator_class"]:
                locator_value = self._build_uiselector(locator_type, locator_value)

            locator = (locator_map[locator_type], locator_value)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found with {locator_type}: {locator_value}")
            return element
        except TimeoutException:
            logger.error(f"Element not found with {locator_type}: {locator_value} within {timeout}s")
            raise
        except Exception as e:
            logger.error(f"Error waiting for element: {str(e)}")
            raise

    def get_element(self, locator_value, locator_type, timeout=10, poll_frequency=0.5):
        """Get an element by its locator."""
        try:
            return self.wait_for_element(locator_value, locator_type, timeout, poll_frequency)
        except TimeoutException:
            logger.error(f"Element not found with {locator_type}: {locator_value} within {timeout}s")
            raise
        except Exception as e:
            logger.error(f"An error occurred while getting element: {str(e)}")
            raise

    def click_element(self, locator_value, locator_type, timeout=10, poll_frequency=0.5):
        """Click an element by its locator."""
        try:
            element = self.get_element(locator_value, locator_type, timeout, poll_frequency)
            element.click()
            logger.info(f"Clicked element with {locator_type}: {locator_value}")
        except NoSuchElementException:
            logger.error(f"Element not clickable with {locator_type}: {locator_value}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while clicking element: {str(e)}")
            raise

    def send_text(self, locator_value, locator_type, text, timeout=10, poll_frequency=0.5):
        """Send text to an element."""
        try:
            element = self.get_element(locator_value, locator_type, timeout, poll_frequency)
            element.clear()
            element.send_keys(text)
            logger.info(f"Sent text '{text}' to element with {locator_type}: {locator_value}")
        except NoSuchElementException:
            logger.error(f"Element not interactable with {locator_type}: {locator_value}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while sending text: {str(e)}")
            raise

    def is_displayed(self, locator_value, locator_type, timeout=10, poll_frequency=0.5):
        """Check if an element is displayed."""
        try:
            element = self.get_element(locator_value, locator_type, timeout, poll_frequency)
            is_visible = element.is_displayed()
            logger.info(f"Element with {locator_type}: {locator_value} is displayed: {is_visible}")
            return is_visible
        except TimeoutException:
            logger.warning(f"Element not found with {locator_type}: {locator_value} within {timeout}s")
            return False
        except Exception as e:
            logger.error(f"Error checking if element is displayed: {str(e)}")
            return False

    def screen_shot(self, screenshot_name):
        """Capture a screenshot and save it."""
        try:
            if not os.path.exists(SCREENSHOT_DIR):
                os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{screenshot_name}_{timestamp}"
            file_path = os.path.join(SCREENSHOT_DIR, f"{file_name}.png")
            if self.driver.get_screenshot_as_file(file_path):
                logger.info(f"Screenshot saved successfully: {file_path}")
                return file_path  # Changed to return path for consistency with your framework
            else:
                logger.error(f"Failed to save screenshot: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            return None

    def _build_uiselector(self, locator_type, locator_value):
        """Build a UiSelector string for Android UIAutomator based on locator type."""
        if locator_type in ["text", "uiautomator_text"]:
            return f'new UiSelector().text("{locator_value}")'
        elif locator_type == "uiautomator_desc":
            return f'new UiSelector().description("{locator_value}")'
        elif locator_type == "uiautomator_class":
            return f'new UiSelector().className("{locator_value}")'
        return locator_value

    def get_element_text(self, locator_value, locator_type, timeout=10, poll_frequency=0.5):
        """Get the text of an element."""
        try:
            element = self.get_element(locator_value, locator_type, timeout, poll_frequency)
            text = element.text
            logger.info(f"Retrieved text '{text}' from element with {locator_type}: {locator_value}")
            return text
        except NoSuchElementException:
            logger.error(f"Element not found with {locator_type}: {locator_value}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving text from element: {str(e)}")
            raise

    def get_element_attribute(self, locator_value, locator_type, attribute="text", timeout=5, poll_frequency=0.5):
        """Get a specific attribute of an element (e.g., 'value' for input fields)."""
        try:
            element = self.get_element(locator_value, locator_type, timeout, poll_frequency)
            attr_value = element.get_attribute(attribute)
            logger.info(f"Retrieved attribute '{attribute}' with value '{attr_value}' from element with {locator_type}: {locator_value}")
            return attr_value
        except NoSuchElementException:
            logger.error(f"Element not found with {locator_type}: {locator_value}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving attribute '{attribute}' from element: {str(e)}")
            raise

    def is_field_populated(self, locator_value, locator_type, attribute="text"):
        """Check if a field is non-empty."""
        try:
            actual_value = self.get_element_attribute(locator_value, locator_type, attribute)
            is_populated = bool(actual_value and actual_value.strip())
            logger.info(
                f"Field with {locator_type}: {locator_value} has value '{actual_value}', is non-empty: {is_populated}")
            return is_populated
        except Exception as e:
            logger.error(f"Error checking field population: {str(e)}")
            return False
    def keyCode(self, value):
        self.driver.press_keycode(value)
        logger.debug(f"Pressed keycode: {value}")