import flask
from flask import Blueprint, render_template, make_response, request, flash, redirect, url_for

from services.integrity_service import IntegrityService
from utils.constants import Constants
from utils.decorator_utils import Decorators
from utils.flask_inject import inject
from utils.utils import Utils

variables = Blueprint('variables', __name__, template_folder='templates')


@variables.route('/initial-setup', methods=['GET', 'POST'])
@Decorators.session_exist
@inject('utils', 'integrity_service')
def initial_setup(utils: Utils, integrity_service: IntegrityService):
    if flask.request.method == 'POST':
        integrity_service.create_calc_storage_file(
            calculation_id=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME)
        )
        integrity_service.save_initial_variable(
            calculation_id=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME),
            form=request.form
        )
        response = redirect(url_for('variables.continue_setting_up'))
        response.set_cookie(
            Constants.PAGE_COUNTER_COOKIE_NAME,
            str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) + 1))
        return response
    else:
        response = make_response(
            render_template(
                'variables/variable_page.html',
                variable_number='1',
                variable_title=Constants.VARIABLES_DESCRIPTION.get('1').get('variable_title'),
                variable_name=Constants.VARIABLES_DESCRIPTION.get('1').get('variable_name'),
                lower_bound=Constants.VARIABLES_DESCRIPTION.get('1').get('lower_bound'),
                upper_bound=Constants.VARIABLES_DESCRIPTION.get('1').get('upper_bound'),
                form_action_url='variables.initial_setup'
            )
        )
        response.set_cookie(Constants.CONSISTENCY_COOKIE_NAME, utils.generate_calculation_id())
        response.set_cookie(Constants.PAGE_COUNTER_COOKIE_NAME, '1')
        return response


@variables.route('/continue-setup', methods=['GET', 'POST'])
@inject('utils', 'integrity_service')
def continue_setting_up(utils: Utils, integrity_service: IntegrityService):
    if flask.request.method == 'POST':
        integrity_service.append_variable(
            calculation_id=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME),
            form=request.form
        )
        response = redirect(url_for('variables.continue_setting_up'))
        response.set_cookie(
            Constants.PAGE_COUNTER_COOKIE_NAME,
            str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) + 1))
        return response
    else:
        if not utils.check_cookie_exists(cookie_value=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME)) \
                or not utils.check_cookie_exists(cookie_value=request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)):
            flash(u'Невозможно найти начальную запись. Заполните значения для 1 переменной заново.')
            return redirect(url_for('main.index'))
        response = make_response(
            render_template(
                'variables/variable_page.html',
                variable_number=request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME),
                variable_title=Constants.VARIABLES_DESCRIPTION.get(
                    request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)).get('variable_title'),
                variable_name=Constants.VARIABLES_DESCRIPTION.get(
                    request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)).get('variable_name'),
                lower_bound=Constants.VARIABLES_DESCRIPTION.get(
                    request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)).get('lower_bound'),
                upper_bound=Constants.VARIABLES_DESCRIPTION.get(
                    request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)).get('upper_bound'),
                form_action_url='variables.continue_setting_up'
            )
        )
        return response
