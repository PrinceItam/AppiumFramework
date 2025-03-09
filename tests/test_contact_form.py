# AppiumFramework/tests/test_contact_form_test.py

import pytest
import allure
from assertpy import assert_that
from faker import Faker
from src.utilities.assertions import Assertions
from src.pages.contact_us_form_page import ContactForm
from src.pages.base_page import BasePage

@pytest.mark.usefixtures("driver")  # Ensure driver is available
class TestContactForm:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.cf = ContactForm(driver)
        self.assertions = Assertions()

    @pytest.fixture
    def ensure_base_screen(self):
        """Ensure the app is on the base screen with the Contact button visible."""
        contact_button_id = "Btn2"
        if not self.cf.is_displayed(contact_button_id, "accessibility_id", timeout=5):
            self.cf.keyCode(4)  # Back navigation to reset state
        assert self.cf.is_displayed(contact_button_id, "accessibility_id", timeout=10), "Base screen not reached"
        return True

    @pytest.fixture
    def open_contact_form(self, ensure_base_screen):
        """Open the Contact Us form from the base screen."""
        self.cf.click_contact_from_button()
        return self.cf.verify_contact_page()

    @allure.title("Verify Contact Us Button is Visible on Base Screen")
    @allure.description("Check that the Contact Us button is displayed on the base screen.")
    @allure.story("Form Accessibility")
    @pytest.mark.order(1)
    def test_contact_button_visible(self, ensure_base_screen):
        """Test only that the Contact button is visible."""
        self.assertions.assert_true(ensure_base_screen, "Contact button should be visible on base screen")

    @allure.title("Open Contact Us Form")
    @allure.description("Verify that clicking the Contact Us button opens the form.")
    @allure.story("Form Accessibility")
    @pytest.mark.order(2)
    def test_open_contact_form(self, ensure_base_screen):
        """Test only the action of opening the form."""
        self.cf.click_contact_from_button()
        form_element = self.cf.verify_contact_page()
        self.assertions.assert_element_visible(form_element, "Contact Us form should be visible after clicking button")

    @allure.title("Enter Contact Us Form Data")
    @allure.description("Enter fake data into the Contact Us form fields.")
    @allure.story("Form Submission")
    @pytest.mark.order(3)
    def test_enter_contact_form_data(self, open_contact_form):
        """Test only entering data into the form."""
        fake = Faker()
        fake_name = fake.name()
        fake_email = fake.email()
        fake_address = fake.address().replace("\n", ", ")
        fake_phone = fake.phone_number()

        self.cf.enter_name(fake_name)
        #name_value = self.cf.get_element_attribute(self.cf._enter_name, "id", "text")
        #assert_that(name_value).is_not_empty().is_equal_to(fake_name)
        self.cf.enter_email(fake_email)
        self.cf.enter_address(fake_address)
        self.cf.enter_mobile_number(fake_phone)
        self.cf.click_submit_button()
        self.cf.screen_shot("contact_form_submission")


