from flask import render_template
from app import app

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='What makes a good beer?')

@app.route('/styles.html')
def styles():
    return render_template('styles.html', title='Styles and Beer')

@app.route('/base.html')
def base():
    return render_template('base.html', title='Base')
