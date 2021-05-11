import flask
from flask import Blueprint, render_template, make_response, request, redirect, url_for

from services.polynomial_service import PolynomialService
from utils.constants import Constants
from utils.decorator_utils import session_exist_for_post_only, session_exist_for_get_post
from utils.flask_inject import inject
from utils.utils import Utils

variables = Blueprint('variables', __name__, template_folder='templates')


@variables.route('/initial-setup', methods=['GET', 'POST'])
@inject('utils', 'polynomial_service')
@session_exist_for_post_only
def initial_setup(utils: Utils, polynomial_service: PolynomialService):
    if flask.request.method == 'POST':
        polynomial_service.create_calc_storage_file(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        )
        polynomial_service.save_initial_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME),
            form=request.form
        )
        response = redirect(url_for('variables.continue_setting_up'))
        response.set_cookie(
            Constants.PAGE_COUNTER_COOKIE_NAME,
            str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) + 1)
        )
        return response
    else:
        response = make_response(
            render_template(
                'variables/polynomial_coefficients_page.html',
                variable_number='1',
                variable_title=Constants.VARIABLES_DESCRIPTION.get('1').get('variable_title'),
                variable_name=Constants.VARIABLES_DESCRIPTION.get('1').get('variable_name'),
                lower_bound=Constants.VARIABLES_DESCRIPTION.get('1').get('lower_bound'),
                upper_bound=Constants.VARIABLES_DESCRIPTION.get('1').get('upper_bound'),
                form_action_url='variables.initial_setup'
            )
        )
        response.set_cookie(Constants.CALCULATION_ID_COOKIE_NAME, utils.get_current_timestamp_millis())
        response.set_cookie(Constants.PAGE_COUNTER_COOKIE_NAME, '1')
        return response


@variables.route('/continue-setup', methods=['GET', 'POST'])
@inject('polynomial_service')
@session_exist_for_get_post
def continue_setting_up(polynomial_service: PolynomialService):
    if flask.request.method == 'POST':
        polynomial_service.append_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME),
            form=request.form
        )
        redirect_url: str = 'variables.final_setup' \
            if request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME) == Constants.LAST_VARIABLE_NUMBER \
            else 'variables.continue_setting_up'
        response = redirect(url_for(redirect_url))
        response.set_cookie(
            Constants.PAGE_COUNTER_COOKIE_NAME,
            str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) + 1)
        )
        return response
    else:
        counter_cookie_value: str = request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)

        if int(counter_cookie_value) >= int(Constants.FINAL_SETUP_NUMBER):
            return redirect(url_for('variables.final_setup'))

        response = make_response(
            render_template(
                'variables/polynomial_coefficients_page.html',
                variable_number=counter_cookie_value,
                variable_title=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('variable_title'),
                variable_name=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('variable_name'),
                lower_bound=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('lower_bound'),
                upper_bound=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('upper_bound'),
                form_action_url='variables.continue_setting_up'
            )
        )
        return response


@variables.route('/final-setup', methods=['GET', 'POST'])
@inject('polynomial_service')
@session_exist_for_get_post
def final_setup(polynomial_service: PolynomialService):
    if flask.request.method == 'POST':
        print('aga')
    else:
        polynomial_service.reformat_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        )
        return render_template('variables/initial_variable_values_page.html')
