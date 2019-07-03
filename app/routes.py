from flask import render_template
from app import app
from app.forms import ReviewForm

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

@app.route('/review.html')
def review():
    form = ReviewForm()
    return render_template('review.html', title='Check a Review', form=form)

@app.route('/base.html')
def base():
    return render_template('base.html', title='Base')
