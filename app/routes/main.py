# Routes
from flask import render_template, Blueprint, request

from utils.constants import Constants
from utils.flask_inject import inject
from utils.utils import Utils

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@inject('utils')
def index(utils: Utils):
    calculation_id_cookie_value: str = request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
    counter_cookie_value: str = request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)
    session_already_exist: bool = utils.check_cookie_exists(cookie_value=calculation_id_cookie_value) \
                                  and utils.check_cookie_exists(cookie_value=counter_cookie_value)
    return render_template(
        'main/index.html',
        session_already_exist=session_already_exist
    )


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/documents')
def documents():
    return render_template('main/documents.html')
