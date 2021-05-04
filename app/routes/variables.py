from flask import Blueprint, render_template

variables = Blueprint('variables', __name__, template_folder='templates')


@variables.route('/L1')
def L1():
    return render_template('variables/L1.html')
