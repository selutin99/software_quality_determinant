import flask
from flask import Blueprint, render_template, make_response, request, flash, redirect, url_for

from services.integrity_service import IntegrityService
from utils.constants import Constants
from utils.flask_inject import inject
from utils.utils import Utils

variables = Blueprint('variables', __name__, template_folder='templates')


@variables.route('/L1', methods=['GET', 'POST'])
@inject('utils', 'integrity_service')
def L1(utils: Utils, integrity_service: IntegrityService):
    if flask.request.method == 'POST':
        if not utils.check_calculation_id_exists(calculation_id=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME)):
            flash(u'Невозможно найти начальную запись. Заполните значения для 1 переменной заново.')
            return redirect(url_for('main.index'))

        integrity_service.create_calc_storage_file(
            calculation_id=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME)
        )
        return redirect(url_for('variables.L2'))
    else:
        response = make_response(render_template('variables/L1.html'))
        response.set_cookie(Constants.CONSISTENCY_COOKIE_NAME, utils.generate_calculation_id())
        return response


@variables.route('/L2', methods=['GET', 'POST'])
def L2():
    if flask.request.method == 'POST':
        pass

    return render_template('variables/L2.html')
