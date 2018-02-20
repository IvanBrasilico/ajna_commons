from flask import render_template
# TODO: Configure customized CSRF error
# from flask_wtf.csrf import CSRFError
# TODO: Configure customized CSRF error
#  http://flask.pocoo.org/docs/0.12/patterns/packages/
# @app.errorhandler(CSRFError)


def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400
