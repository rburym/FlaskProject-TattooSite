from flask import render_template

from app import app

@app.errorhandler(403)
def error404(e):
    return render_template('errors/error403.html')

@app.errorhandler(404)
def error404(e):
    return render_template('errors/error404.html')

@app.errorhandler(500)
def error500(e):
    return render_template('errors/error500.html')
