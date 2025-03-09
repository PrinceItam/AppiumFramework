# src/utilities/assertions.py
class Assertions:
    @staticmethod
    def assert_element_visible(element, message="Element should be visible"):
        """Assert that an element is visible."""
        assert element, message

    @staticmethod
    def assert_text_equal(actual_text, expected_text, message="Text does not match"):
        """Assert that the actual text matches the expected text."""
        assert actual_text == expected_text, f"{message}: Expected '{expected_text}', got '{actual_text}'"

    @staticmethod
    def assert_true(condition, message="Condition should be true"):
        """Assert that a condition is true."""
        assert condition, message