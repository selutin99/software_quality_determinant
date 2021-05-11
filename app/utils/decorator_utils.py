from functools import wraps, partial
from typing import Callable

import flask
from flask import flash, url_for, request
from werkzeug.utils import redirect

from app import injector
from utils.constants import Constants
from utils.utils import Utils


class Decorators:
    @staticmethod
    def session_exist(func: Callable, methods: list) -> Callable:
        @wraps(func)
        def decorated_view(*args, **kwargs):
            utils: Utils = injector.get('utils')
            calculation_id_cookie_exist: bool = utils.check_cookie_exists(
                cookie_value=request.cookies.get(Constants.CALCULATION_ID_COOKIE_NAME)
            )
            counter_cookie_exist: bool = utils.check_cookie_exists(
                cookie_value=request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)
            )
            if flask.request.method not in methods:
                return func(*args, **kwargs)
            elif calculation_id_cookie_exist and counter_cookie_exist:
                return func(*args, **kwargs)
            else:
                flash(u'Невозможно найти начальную запись. Заполните значения для 1 переменной заново.')
                return redirect(url_for('main.index'))

        return decorated_view


session_exist_for_post_only = partial(Decorators.session_exist, methods=['POST'])
session_exist_for_get_only = partial(Decorators.session_exist, methods=['GET'])
session_exist_for_get_post = partial(Decorators.session_exist, methods=['GET', 'POST'])
