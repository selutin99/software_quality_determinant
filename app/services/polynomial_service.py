import json
from typing import NoReturn

from werkzeug.datastructures import ImmutableMultiDict

from ..services.custom_exceptions.polynomial_service_custom_exceptions import PolynomialServiceCustomExceptions
from ..utils.constants import Constants
from ..utils.utils import Utils


class PolynomialService:
    def __init__(self, utils: Utils):
        self.__utils = utils

        self.__polynomial_coefficients_key = 'polynomial_coefficients'

    def create_calc_storage_file(self, calculation_id: str) -> NoReturn:
        """
        Create empty json file with name is equal to current timestamp
        :param calculation_id: cookie value is equal to user session id
        """
        calculation_storage_file = open(
            '{path}{id}.json'.format(
                path=Constants.PATH_TO_CALC_STORAGE_FILE,
                id=calculation_id
            ),
            'w'
        )
        calculation_storage_file.close()

    def save_initial_polynomial_coefficients(self, calculation_id: str, form: ImmutableMultiDict) -> NoReturn:
        """
        Save f1-f6 polynomial coefficients to json file
        :param calculation_id: cookie value is equal to user session id
        :param form: html form which contains polynomial coefficients
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'a') as file:
            result_dictionary: dict = self.__parse_polynomial_coefficients(form=form)
            json.dump(result_dictionary, file, indent=4)

    def append_polynomial_coefficients(self, calculation_id: str, form: ImmutableMultiDict) -> NoReturn:
        """
        Save f7-f98 polynomial coefficients to json file
        :param calculation_id: cookie value is equal to user session id
        :param form: html form which contains polynomial coefficients
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)

        result_dictionary: dict = self.__parse_polynomial_coefficients(form=form)
        data.update(result_dictionary)

        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'w') as file:
            json.dump(data, file, indent=4)

    def reformat_polynomial_coefficients(self, calculation_id: str) -> NoReturn:
        """
        Add root key 'polynomial_coefficients' to result json
        :param calculation_id: cookie value is equal to user session id
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)

        if self.__polynomial_coefficients_key not in data:
            data: dict = {self.__polynomial_coefficients_key: data}

            with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'w') as file:
                json.dump(data, file, indent=4)

    def __parse_polynomial_coefficients(self, form: ImmutableMultiDict) -> dict:
        result_dict: dict = dict()
        for field in form.items():
            try:
                # Get current variable, function, and coefficients
                parsed_list: list = self.__utils.split_by_numbers(field[0])
                # Append polynomial function to variable
                if ('f' + parsed_list[1]) not in result_dict:
                    result_dict['f' + parsed_list[1]] = {}
                # Append polynomial coefficients to function
                result_dict['f' + parsed_list[1]]['A' + parsed_list[2]] = field[1]
            except Exception:
                raise PolynomialServiceCustomExceptions.ParsingException('Parsing exception')
        return result_dict
