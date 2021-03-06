import ast
import os

import flask
import pdfkit
from flask import Blueprint, render_template, make_response, request, redirect, url_for

from ..services.calculation_service import CalculationService
from ..services.polynomial_service import PolynomialService
from ..utils.constants import Constants
from ..utils.decorator_utils import session_exist_for_post_only, session_exist_for_get_post, session_exist_for_get_only
from ..utils.flask_inject import inject
from ..utils.utils import Utils

calculation = Blueprint('calculation', __name__, template_folder='templates')


@calculation.route('/initial-setup', methods=['GET', 'POST'])
@inject('utils', 'polynomial_service')
@session_exist_for_post_only
def initial_setup(utils: Utils,
                  polynomial_service: PolynomialService):
    if flask.request.method == 'POST':
        polynomial_service.create_calc_storage_file(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        )
        polynomial_service.save_initial_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME),
            form=request.form
        )
        response = redirect(url_for('calculation.continue_setting_up'))
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
                form_action_url='calculation.initial_setup'
            )
        )
        response.set_cookie(Constants.CALCULATION_ID_COOKIE_NAME, utils.get_current_timestamp_millis())
        response.set_cookie(Constants.PAGE_COUNTER_COOKIE_NAME, '1')
        return response


@calculation.route('/continue-setup', methods=['GET', 'POST'])
@inject('polynomial_service')
@session_exist_for_get_post
def continue_setting_up(polynomial_service: PolynomialService):
    if flask.request.method == 'POST':
        polynomial_service.append_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME),
            form=request.form
        )
        redirect_url: str = 'calculation.final_setup' \
            if request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME) == Constants.LAST_VARIABLE_NUMBER \
            else 'calculation.continue_setting_up'
        response = redirect(url_for(redirect_url))
        response.set_cookie(
            Constants.PAGE_COUNTER_COOKIE_NAME,
            str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) + 1)
        )
        return response
    else:
        counter_cookie_value: str = request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)
        # Redirect to set initial variables page if counter cookie >= 16
        if int(counter_cookie_value) >= int(Constants.FINAL_SETUP_NUMBER):
            return redirect(url_for('calculation.final_setup'))
        response = make_response(
            render_template(
                'variables/polynomial_coefficients_page.html',
                variable_number=counter_cookie_value,
                variable_title=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('variable_title'),
                variable_name=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('variable_name'),
                lower_bound=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('lower_bound'),
                upper_bound=Constants.VARIABLES_DESCRIPTION.get(counter_cookie_value).get('upper_bound'),
                form_action_url='calculation.continue_setting_up'
            )
        )
        return response


@calculation.route('/final-setup', methods=['GET', 'POST'])
@inject('polynomial_service', 'calculation_service')
@session_exist_for_get_post
def final_setup(polynomial_service: PolynomialService,
                calculation_service: CalculationService):
    if flask.request.method == 'POST':
        calculation_service.append_initial_variable_values(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME),
            form=request.form
        )
        t1_solve: dict = calculation_service.solve_difference_equations(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        )
        return redirect(url_for('calculation.cancel_calculation', solve=t1_solve))
    else:
        polynomial_service.reformat_polynomial_coefficients(
            calculation_id=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        )
        return render_template('variables/initial_variable_values_page.html')


@calculation.route('/cancel-calculation', methods=['GET', 'POST'])
@inject('calculation_service')
@session_exist_for_get_post
def cancel_calculation(calculation_service: CalculationService):
    if flask.request.method == 'POST':
        return redirect(url_for('main.clear_session'))
    else:
        calculation_id: str = request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
        polynomial_coefficients, initial_variable_values = calculation_service.get_input_user_parameters(
            calculation_id=calculation_id
        )
        return render_template(
            'variables/result_report.html',
            plot_name=calculation_id,
            polynomial_coefficients=polynomial_coefficients,
            initial_variable_values=initial_variable_values,
            t1_solution=enumerate(ast.literal_eval(request.args.get('solve')).get('solution')),
            t1_pdf_list={'t1_sol': ast.literal_eval(request.args.get('solve')).get('solution')}
        )


@calculation.route('/decrease', methods=['GET'])
@session_exist_for_get_only
def decrease_counter():
    response = redirect(url_for('calculation.continue_setting_up'))
    response.set_cookie(
        Constants.PAGE_COUNTER_COOKIE_NAME,
        str(int(request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)) - 1)
    )
    return response


@calculation.route('/get-pdf', methods=['GET'])
@inject('calculation_service')
@session_exist_for_get_only
def get_generated_pdf(calculation_service: CalculationService):
    calculation_id: str = request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
    polynomial_coefficients, initial_variable_values = calculation_service.get_input_user_parameters(
        calculation_id=calculation_id
    )
    css = ['app/static/css/bootstrap_for_pdfkit/bootstrap.min.css']
    options = {
        'enable-local-file-access': None,
        'encoding': 'UTF-8'
    }

    rendered = render_template(
        'variables/pdf_template.html',
        plot_path=os.path.abspath(Constants.PATH_SOLUTION_GRAPHS_IMAGE + calculation_id + '.png'),
        perturbations_graph_path=os.path.abspath(Constants.PATH_TO_IMAGES_STORAGE_FILE + 'perturbations/perturbations_graph.png'),
        perturbations_equations_path=os.path.abspath(Constants.PATH_TO_IMAGES_STORAGE_FILE + 'perturbations/perturbations_equations.png'),
        petal_path=os.path.abspath(Constants.PATH_PETAL_GRAPHS_IMAGE) + '/' + calculation_id + '/',
        polynomial_coefficients=polynomial_coefficients,
        initial_variable_values=initial_variable_values,
        t1_solution=enumerate(ast.literal_eval(request.args.get('t1_solution')).get('t1_sol'))
    )
    pdf = pdfkit.from_string(rendered, False, css=css, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
    return response
