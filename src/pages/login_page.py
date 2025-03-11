from src.pages.base_page import BasePage  # Adjusted import path
import allure
from src.utilities.custom_logger import CustomLogger as cl  # Adjusted import path

class LoginPage(BasePage):
    """Represents the login page of the application."""

    def __init__(self, driver):
        """Initializes the LoginPage with a driver instance."""
        super().__init__(driver)
        self.log = cl.get_logger(__name__)  # Corrected logger initialization

        # Locators
        self._login_button = "Btn6"
        self._email_input = "com.code2lead.kwad:id/Et4"
        self._password_input = "com.code2lead.kwad:id/Et5"
        self._login_submit_button = "com.code2lead.kwad:id/Btn3"
        self._wrong_credentials_message = "Wrong Credentials"
        self._admin_page_title = "Enter Admin"
        self._admin_text_input = "com.code2lead.kwad:id/Edt_admin"
        self._admin_submit_button = "SUBMIT"

    @allure.step("Click login button")
    def click_login_button(self):
        """Clicks the login button."""
        self.click_element(self._login_button, "accessibility_id")
        self.log.info("Clicked login button")  # Using logger directly; allureLogs is optional


    @allure.step("Enter email: {email}")
    def enter_email(self, email):
        """Enters the email address."""
        self.send_text(self._email_input, "id", email)
        self.log.info(f"Entered email: {email}")


    @allure.step("Enter password: {password}")
    def enter_password(self, password):
        """Enters the password."""
        self.send_text(self._password_input, "id", password)
        self.log.info(f"Entered password: {password}")


    @allure.step("Click login submit button")
    def click_login_submit(self):
        """Clicks the login submit button."""
        self.click_element(self._login_submit_button, "id")
        self.log.info("Clicked login submit button")


    @allure.step("Verify admin screen is displayed")
    def verify_admin_screen_displayed(self):
        """Verifies that the admin screen is displayed."""
        is_displayed = self.is_displayed(self._admin_page_title, "text")
        assert is_displayed, "Admin screen not displayed"  # Simplified assertion
        self.log.info("Verified admin screen is displayed")


    @allure.step("Enter admin text: {text}")
    def enter_admin_text(self, text="Code2lead"):
        """Enters text into the admin text input."""
        self.send_text(self._admin_text_input, "id", text)
        self.log.info(f"Entered admin text: {text}")


    @allure.step("Click admin submit button")
    def click_admin_submit(self):
        """Clicks the admin submit button."""
        self.click_element(self._admin_submit_button, "text")
        self.log.info("Clicked admin submit button")


    @allure.step("Verify wrong credentials message is displayed")
    def verify_wrong_credentials_message_displayed(self):
        """Verifies that the wrong credentials message is displayed."""
        is_displayed = self.is_displayed(self._wrong_credentials_message, "text")
        assert is_displayed, "Wrong credentials message is not displayed"
        self.log.info("Verified wrong credentials message is displayed")
