import re
import time


class Utils:
    def get_current_timestamp_millis(self) -> str:
        """
        Generate id based on current time in millis
        and convert it to str
        :return: generated string timestamp in millis
        """
        return str(round(time.time() * 1000))

    def check_cookie_exists(self, cookie_value: str) -> bool:
        """
        Check cookie is not None
        :param cookie_value: cookie value
        :return: cookie exist in session or not
        """
        return cookie_value not in (None, '')

    def split_by_numbers(self, input_string: str) -> list:
        """
        Return list of numbers which contains in string.
        For example: L1f2A0 -> [1, 2, 0]
        :param input_string: string which contains letters and numbers
        :return: list of numbers
        """
        if input_string:
            return re.findall(r'\d+', input_string)
