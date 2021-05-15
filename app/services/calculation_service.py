import json
import math
from typing import NoReturn

import numpy as np
from werkzeug.datastructures import ImmutableMultiDict

from services.custom_exceptions.calculation_service_custom_exceptions import CalculationServiceCustomExceptions
from utils.constants import Constants
from utils.utils import Utils


class CalculationService:
    def __init__(self, utils: Utils):
        self.__utils = utils

        self.__data_dict: dict = {}
        self.__polynomial_coefficients_key = 'polynomial_coefficients'
        self.__initial_variable_values_key = 'initial_variable_values'

    def solve_difference_equations(self, calculation_id: str) -> dict:
        """
        Solving a system of differential equations
        in accordance with the developed mathematical model
        and the parameters entered by the user for the current session
        :param calculation_id: cookie value is equal to user session id
        :return: dictionary which contains all input user parameters
        and path to image -> solution for system of differential equations
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)
            self.__data_dict = data

        return {}

    def append_initial_variable_values(self, calculation_id: str, form: ImmutableMultiDict) -> NoReturn:
        """
        Add root key 'initial_variable_values' to result json
        :param calculation_id: cookie value is equal to user session id
        :param form: requested form with initial varibles values
        """
        calculation_storage_file_path: str = '{path}{id}.json'.format(
            path=Constants.PATH_TO_CALC_STORAGE_FILE,
            id=calculation_id
        )
        with open(calculation_storage_file_path, 'r') as file:
            data = json.load(file)

        if self.__initial_variable_values_key not in data:
            result_dictionary: dict = {self.__initial_variable_values_key: self.__parse_initial_values(form=form)}
            data.update(result_dictionary)

            with open(calculation_storage_file_path, 'w') as file:
                json.dump(data, file, indent=4)

    def __parse_initial_values(self, form: ImmutableMultiDict) -> dict:
        result_dict: dict = dict()
        for field in form.items():
            try:
                result_dict[field[0]] = field[1]
            except Exception:
                raise CalculationServiceCustomExceptions.ParsingException('Parsing exception')
        return result_dict

    def __describe_systems_of_differencials_equation(self, y, x) -> list:
        # Get polynomial coefficients
        cf: dict = self.__get_polynomial_coefficients()

        # Perturbations
        q1 = 0.4 if x > 0.5 else 0.3
        q2 = 0.15 * math.cos(x)
        q3 = 0.15 * math.sin(x)
        q4 = 0.4 if x > 0.8 else 0.3
        q5 = 0.25 * math.sin(x)

        # Variables
        dL1 = \
            self.__multiplicate_polynomials(
                variable_number='1',
                lower_polynomial_bound=1,
                upper_polynomial_bound=7,
                cf=cf,
                y=y,
                is_incremental=True
            ) * (q1 + q2) - q3
        dL2 = \
            self.__multiplicate_polynomials(
                variable_number='2',
                lower_polynomial_bound=7,
                upper_polynomial_bound=12,
                cf=cf,
                y=y,
                is_incremental=True
            ) * (q2 + q5) - q4
        dL3 = -y[0] * y[2] - (1 - y[1] * y[1])

        return [dL1, dL2, dL3, dL4, dL5, dL6, dL7, dL8, dL9, dL10, dL11, dL12, dL13, dL14, dL15]

    def __get_initial_variable_values(self, session_data_variable_values: dict) -> np.array:
        return np.array(list(session_data_variable_values.values()))

    def __get_polynomial_coefficients(self) -> dict:
        return self.__data_dict.get(self.__polynomial_coefficients_key)

    def __multiplicate_polynomials(self,
                                   variable_number: str,
                                   lower_polynomial_bound: int,
                                   upper_polynomial_bound: int,
                                   cf: dict,
                                   y,
                                   is_incremental: bool = True) -> float:
        multiplication_result: float = 1.0
        polynomial_coefficients: list = list(range(lower_polynomial_bound, upper_polynomial_bound))
        related_variables: list = Constants.VARIABLES_DESCRIPTION \
            .get(variable_number) \
            .get('incremental_related_variables' if is_incremental else 'decremental_related_variables')

        for variable_number, polynomial_coefficient in zip(related_variables, polynomial_coefficients):
            multiplication_result *= \
                cf['f' + str(polynomial_coefficient)]['A0'] + \
                cf['f' + str(polynomial_coefficient)]['A1'] * y[variable_number] + \
                cf['f' + str(polynomial_coefficient)]['A2'] * (y[variable_number] ** 2)

        return multiplication_result
