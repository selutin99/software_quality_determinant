import time


class Utils:
    def generate_calculation_id(self) -> str:
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
