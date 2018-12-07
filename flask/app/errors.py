from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(error)
    return render_template('404.j2'), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error("Rolling back because:\n" + str(error))
    db.session.rollback()
    return render_template('500.j2'), 500
