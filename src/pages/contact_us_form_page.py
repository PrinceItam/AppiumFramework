from src.pages.base_page import BasePage
import allure

class ContactForm(BasePage):
    _contact_from_button = "Btn2"  # accessibilityID
    _page_title = "Contact Us form"  # Text
    _enter_name = "Enter Name"  # text
    _enter_email = "Enter Email"  # text
    _enter_address = "Enter Address"  # text
    _enter_mobile_number = "Enter Mobile No"  # text
    _submit_button = "SUBMIT"

    @allure.step("Click Contact Form button")
    def click_contact_from_button(self):
        self.click_element(self._contact_from_button, "accessibility_id")

    @allure.step("Verify Contact Page is displayed")
    def verify_contact_page(self):
        element = self.is_displayed(self._page_title, "text")
        assert element, "Contact Us form page title not displayed"
        return element  # Return for clarity in test assertions if needed

    @allure.step("Enter Name: {text}")
    def enter_name(self, text="Code2Lead"):
        self.send_text(self._enter_name, "text", text)

    @allure.step("Enter Email: {text}")
    def enter_email(self, text):
        self.send_text(self._enter_email, "text", text)

    @allure.step("Enter Address: {text}")
    def enter_address(self, text):
        self.send_text(self._enter_address, "text", text)

    @allure.step("Enter Mobile Number: {text}")
    def enter_mobile_number(self, text):
        self.send_text(self._enter_mobile_number, "text", text)

    @allure.step("Click Submit Button")
    def click_submit_button(self):
        self.click_element(self._submit_button, "text")