# Routes
from flask import render_template, Blueprint

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    return render_template('main/about.html')


@main.route('/documents')
def documents():
    return render_template('main/documents.html')
