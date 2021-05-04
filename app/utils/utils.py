import time


class Utils:
    def generate_calculation_id(self) -> str:
        """
        Generate id based on current time in millis
        and convert it to str
        :return: generated string timestamp in millis
        """
        return str(round(time.time() * 1000))

    def check_calculation_id_exists(self, calculation_id: str) -> bool:
        """
        Check cookie calculation id is not None
        :param calculation_id: calculation id cookie
        :return: calculation id cookie exist in session or not
        """
        return calculation_id not in (None, '')
