from datetime import datetime, timedelta
import unittest


class MyTest(unittest.TestCase):
    def test__testable_function__is_correct(self) -> None:
        # Arrange
        current_time = datetime(1970, 1, 1, 13, 00)

        # Act
        result = current_time + timedelta(hours=1)

        # Assert
        expected_result = datetime(1970, 1, 1, 14, 00)
        assert expected_result == result
