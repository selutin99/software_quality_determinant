from flask import render_template, url_for, redirect, flash

from app import app
from ..services.custom_exceptions.calculation_service_custom_exceptions import CalculationServiceCustomExceptions
from ..services.custom_exceptions.polynomial_service_custom_exceptions import PolynomialServiceCustomExceptions


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(410)
def page_not_avaliable(e):
    return render_template('errors/410.html'), 410


@app.errorhandler(FileNotFoundError)
def handle_base_exception(exception):
    flash(u'Ошибка обработки вашей сессии. Начните ввод данных заново!')
    return redirect(url_for('main.index'))


@app.errorhandler(PolynomialServiceCustomExceptions.ParsingException)
def handle_base_exception(exception):
    flash(u'Ошибка обработки полиномиальных коэффициентов')
    return redirect(url_for('main.index'))


@app.errorhandler(CalculationServiceCustomExceptions.ParsingException)
def handle_base_exception(exception):
    flash(u'Ошибка обработки начальных значений переменных')
    return redirect(url_for('main.index'))


@app.errorhandler(Exception)
def handle_base_exception(exception):
    flash(u'Непредвиденная ошибка')
    return redirect(url_for('main.index'))
