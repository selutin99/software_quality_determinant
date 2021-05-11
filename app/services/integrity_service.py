import json
import re
from typing import NoReturn

from werkzeug.datastructures import ImmutableMultiDict

from utils.constants import Constants


class IntegrityService:
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

    def save_initial_variable(self, calculation_id: str, form: ImmutableMultiDict) -> NoReturn:
        """
        Save L1 variable to json file
        :param calculation_id: cookie value is equal to user session id
        :param form: html form which contains polynomial coefficients
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'a') as file:
            result_dictionary: dict = self.__parse_input_arguments(form=form)
            json.dump(result_dictionary, file, indent=4)

    def append_variable(self, calculation_id: str, form: ImmutableMultiDict) -> NoReturn:
        """
        Save L2-L15 variables to json file
        :param calculation_id: cookie value is equal to user session id
        :param form: html form which contains polynomial coefficients
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)

        result_dictionary: dict = self.__parse_input_arguments(form=form)
        data.update(result_dictionary)

        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'w') as file:
            json.dump(data, file, indent=4)

    def __parse_input_arguments(self, form: ImmutableMultiDict) -> dict:
        result_dict = dict()
        for field in form.items():
            # Get current variable, function, and coefficients
            parsed_list: list = self.__split_by_numbers(field[0])
            # Add variable to result dict
            if ('L' + parsed_list[0]) not in result_dict:
                result_dict['L' + parsed_list[0]] = {}
            # Append polynomial function to variable
            if ('L' + parsed_list[0]) in result_dict and \
                    not result_dict['L' + parsed_list[0]].get('f' + parsed_list[1]):
                result_dict['L' + parsed_list[0]]['f' + parsed_list[1]] = {}
            # Append polynomial coefficients to function
            result_dict['L' + parsed_list[0]]['f' + parsed_list[1]]['A' + parsed_list[2]] = field[1]
        return result_dict

    def __split_by_numbers(self, input_string: str) -> list:
        """
        Return list of numbers which contains in string.
        For example: L1f2A0 -> [1, 2, 0]
        :param input_string: string which contains letters and numbers
        :return: list of numbers
        """
        if input_string:
            return re.findall(r"\d+", input_string)
