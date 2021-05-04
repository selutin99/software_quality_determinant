from flask import render_template, url_for, redirect

from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(410)
def page_not_avaliable(e):
    return render_template('errors/410.html'), 410


# @app.errorhandler(Exception)
# def handle_base_exception(exception):
#     return redirect(url_for('main.index'))
