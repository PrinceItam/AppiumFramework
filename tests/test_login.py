# AppiumFramework/tests/test_login.py

import pytest
import allure
from src.pages.base_page import BasePage
from src.pages.login_page import LoginPage

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.lp = LoginPage(driver)
        self.bp = BasePage(driver)

    def ensure_login_screen(self):
        if not self.bp.is_displayed("Btn6", "accessibility_id", timeout=5):
            self.bp.keyCode(4)  # Back navigation as fallback
        assert self.bp.is_displayed("Btn6", "accessibility_id", timeout=10), "Login screen not reached"

    @pytest.mark.parametrize("email, password", [("wrong@example.com", "wrongpassword")])
    @allure.title("Test failed login with invalid credentials")
    def test_failed_login(self, email, password):
        self.ensure_login_screen()
        self.lp.click_login_button()
        self.lp.enter_email(email)
        self.lp.enter_password(password)
        self.lp.click_login_submit()
        self.lp.verify_wrong_credentials_message_displayed()

    @pytest.mark.parametrize("email, password, admin_text", [("admin@gmail.com", "admin123", "AdminTest")])
    @allure.title("Test successful login with valid credentials")
    def test_successful_login(self, email, password, admin_text):
        self.ensure_login_screen()
        self.lp.click_login_button()
        self.lp.enter_email(email)
        self.lp.enter_password(password)
        self.lp.click_login_submit()
        self.lp.verify_admin_screen_displayed()

    @pytest.mark.parametrize("email, password, admin_text", [("admin@gmail.com", "admin123", "AdminTest")])
    @allure.title("Test admin text entry after successful login")
    def test_enter_admin_in_edit_box(self, email, password, admin_text):
        self.lp.verify_admin_screen_displayed()
        self.lp.enter_admin_text(admin_text)
        self.lp.click_admin_submit()