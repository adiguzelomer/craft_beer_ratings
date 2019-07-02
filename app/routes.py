from flask import render_template
from app import app

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('base.html', title='What makes a good beer?')

@app.route('/desc-stats.html')
def desc_stats():
    return render_template('desc-stats.html', title='Descriptive Statistics')

@app.route('/clustering.html')
def clustering():
    return render_template('clustering.html', title="Clustering")

@app.route('/styles.html')
def styles():
    return render_template('styles.html', title='Styles and Beer')

@app.route('/scatter.html')
def scatter():
    return render_template('scatter.html', title='Scatter')
@app.route('/base.html')
def base():
    return render_template('base.html', title='Base')
