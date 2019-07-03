from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ReviewForm

@app.route('/')
@app.route('/index.html')
def index():
    return render_template(url_for('index'), title='What makes a good beer?')

@app.route('/desc_stats.html')
def desc_stats():
    return render_template(url_for('desc_stats'), title='Descriptive Statistics')

@app.route('/clustering.html')
def clustering():
    return render_template(url_for('clustering'), title="Clustering")

@app.route('/review.html', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        flash('Analyzing your review.')
        flash(form.beer_review.data)
        return redirect(url_for('review'))
    return render_template(url_for('review'), title='Check a Review', form=form)

@app.route('/base.html')
def base():
    return render_template(url_for('base'), title='Base')
