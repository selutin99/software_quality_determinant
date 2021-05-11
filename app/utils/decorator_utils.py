from functools import wraps
from typing import Callable

import flask
from flask import flash, url_for, request
from werkzeug.utils import redirect

from app import injector
from utils.constants import Constants
from utils.utils import Utils


class Decorators:
    @staticmethod
    def session_exist(func: Callable) -> Callable:
        @wraps(func)
        def decorated_view(*args, **kwargs):
            utils: Utils = injector.get('utils')
            calculation_id_cookie_exist: bool = utils.check_cookie_exists(
                cookie_value=request.cookies.get(Constants.CONSISTENCY_COOKIE_NAME)
            )
            counter_cookie_exist: bool = utils.check_cookie_exists(
                cookie_value=request.cookies.get(Constants.PAGE_COUNTER_COOKIE_NAME)
            )
            if flask.request.method == 'POST' and not calculation_id_cookie_exist or not counter_cookie_exist:
                flash(u'Невозможно найти начальную запись. Заполните значения для 1 переменной заново.')
                return redirect(url_for('main.index'))
            else:
                return func(*args, **kwargs)

        return decorated_view
