import json
import math
from typing import NoReturn

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
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

    def get_input_user_parameters(self, calculation_id: str) -> tuple:
        """
        Get input polynomial coefficients & initial variable values
        to display it to user in final report
        :param calculation_id: cookie value is equal to user session id
        :return: polynomial coefficients dictionary and initial variable values dictionary
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)
        return data.get(self.__polynomial_coefficients_key), data.get(self.__initial_variable_values_key)

    def solve_difference_equations(self, calculation_id: str) -> dict:
        """
        Solving a system of differential equations
        in accordance with the developed mathematical model
        and the parameters entered by the user for the current session
        :param calculation_id: cookie value is equal to user session id
        :return: dict which contains all systems solutions for t = 1
        """
        with open('{path}{id}.json'.format(path=Constants.PATH_TO_CALC_STORAGE_FILE, id=calculation_id), 'r') as file:
            data = json.load(file)
            self.__data_dict = data

        Y, X = self.__solve_systems_of_difference_equations(data=self.__data_dict)
        self.__save_plot(calculation_id=calculation_id, Y=Y, X=X)

        return {'solution': [Y[len(Y) - 1, i] for i in range(0, 15)]}

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

    def __save_plot(self, calculation_id: str, Y: np.ndarray, X: np.ndarray) -> NoReturn:
        plot_path: str = Constants.PATH_SOLUTION_GRAPHS_IMAGE + calculation_id + '.png'

        plt.rcParams["figure.figsize"] = (15, 8)

        for i in range(0, 15):
            plt.plot(X, Y[:, i], label='L' + str(i + 1))

        plt.legend()
        plt.savefig(plot_path)

    def __solve_systems_of_difference_equations(self, data: dict) -> tuple:
        X = np.linspace(0, 1, 50)
        Y = None
        niter = 100
        u = 0
        tol = 0.1
        ustep = 0.05

        for i in range(niter):
            u += ustep
            Y = odeint(
                self.__describe_difference_equations,
                self.__get_initial_variable_values(
                    session_data_variable_values=data.get(self.__initial_variable_values_key)
                ),
                X
            )
            if abs(Y[len(Y) - 1, 1] - 1) < tol:
                break
        return Y, X

    def __describe_difference_equations(self, y: np.ndarray, x: float) -> list:
        # Get polynomial coefficients
        cf: dict = self.__get_polynomial_coefficients()

        # Perturbations
        q1 = 0.4 if x > 0.5 else 0.3
        q2 = 0.15 * math.cos(x)
        q3 = 0.15 * math.sin(x)
        q4 = 0.4 if x > 0.8 else 0.3
        q5 = 0.25 * math.sin(x)

        # Variables
        dL1 = self.__multiplicate_polynomials('1', 1, 7, cf, y, is_incremental=True) * (q1 + q2) - q3
        dL2 = self.__multiplicate_polynomials('2', 7, 12, cf, y, is_incremental=True) * (q2 + q5) - q4
        dL3 = self.__multiplicate_polynomials('3', 12, 19, cf, y, is_incremental=True) * q2 - q5
        dL4 = self.__multiplicate_polynomials('4', 19, 28, cf, y, is_incremental=True) * q2 \
              - self.__multiplicate_polynomials('4', 28, 29, cf, y, is_incremental=False)
        dL5 = self.__multiplicate_polynomials('5', 29, 36, cf, y, is_incremental=True) * (q1 + q2 + q3) \
              - self.__multiplicate_polynomials('5', 36, 37, cf, y, is_incremental=False)
        dL6 = self.__multiplicate_polynomials('6', 37, 42, cf, y, is_incremental=True) * (q1 + q3) \
              - self.__multiplicate_polynomials('6', 42, 43, cf, y, is_incremental=False)
        dL7 = self.__multiplicate_polynomials('7', 43, 47, cf, y, is_incremental=True) * (q3 + q4) \
              - self.__multiplicate_polynomials('7', 47, 48, cf, y, is_incremental=False)
        dL8 = self.__multiplicate_polynomials('8', 48, 54, cf, y, is_incremental=True) * q3 \
              - self.__multiplicate_polynomials('8', 54, 56, cf, y, is_incremental=False)
        dL9 = self.__multiplicate_polynomials('9', 56, 58, cf, y, is_incremental=True) * (q1 + q3 + q4) \
              - self.__multiplicate_polynomials('9', 58, 63, cf, y, is_incremental=False)
        dL10 = self.__multiplicate_polynomials('10', 63, 69, cf, y, is_incremental=True) * (q2 + q5) \
               - self.__multiplicate_polynomials('10', 69, 70, cf, y, is_incremental=False)
        dL11 = self.__multiplicate_polynomials('11', 70, 75, cf, y, is_incremental=True) * (q1 + q3) \
               - self.__multiplicate_polynomials('11', 75, 77, cf, y, is_incremental=False)
        dL12 = self.__multiplicate_polynomials('12', 77, 80, cf, y, is_incremental=True) * (q1 + q2 + q5) \
               - self.__multiplicate_polynomials('12', 80, 81, cf, y, is_incremental=False)
        dL13 = self.__multiplicate_polynomials('13', 81, 88, cf, y, is_incremental=True) * (q1 + q2) - q4
        dL14 = self.__multiplicate_polynomials('14', 88, 92, cf, y, is_incremental=True) * (q2 + q3) - q5
        dL15 = self.__multiplicate_polynomials('15', 92, 99, cf, y, is_incremental=True) * (q1 + q2 + q5) - q3

        return [dL1, dL2, dL3, dL4, dL5, dL6, dL7, dL8, dL9, dL10, dL11, dL12, dL13, dL14, dL15]

    def __get_initial_variable_values(self, session_data_variable_values: dict) -> np.array:
        return np.array([float(i) for i in list(session_data_variable_values.values())])

    def __get_polynomial_coefficients(self) -> dict:
        return self.__data_dict.get(self.__polynomial_coefficients_key)

    def __multiplicate_polynomials(self,
                                   variable_number: str,
                                   lower_polynomial_bound: int,
                                   upper_polynomial_bound: int,
                                   cf: dict,
                                   y: np.ndarray,
                                   is_incremental: bool = True) -> float:
        multiplication_result: float = 1.0
        polynomial_coefficients: list = list(range(lower_polynomial_bound, upper_polynomial_bound))
        related_variables: list = Constants.VARIABLES_DESCRIPTION \
            .get(variable_number) \
            .get('incremental_related_variables' if is_incremental else 'decremental_related_variables')

        for variable_number, polynomial_coefficient in zip(related_variables, polynomial_coefficients):
            multiplication_result *= float(cf['f' + str(polynomial_coefficient)]['A0']) + \
                                     float(cf['f' + str(polynomial_coefficient)]['A1']) * y[variable_number] + \
                                     float(cf['f' + str(polynomial_coefficient)]['A2']) * (y[variable_number] ** 2)

        return multiplication_result
