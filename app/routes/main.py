# Routes
from flask import render_template, Blueprint

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/L1')
def L1():
    return render_template('L1.html')
