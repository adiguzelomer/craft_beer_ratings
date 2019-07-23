from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import ReviewForm
from app.analyze_review.analyze_review import ReviewProcessor
from numpy import argmax
from src.popularity.popularity import PopularityRecommender
import pandas as pd

processor = ReviewProcessor()

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
        global processor
        flash('Analyzing your review.')
        flash(form.beer_review.data)
        clean_review = processor.clean_review(form.beer_review.data)
        flash(clean_review)
        tf_idf_vec = processor.get_tfidf_vector(clean_review)
        flash(str(tf_idf_vec))
        topic_vec = processor.get_topic_vector(tf_idf_vec)
        flash(str(topic_vec))
        flash(str(topic_vec.shape))
        for beer in processor.get_top_ten_reviews(argmax(topic_vec))['beer']:
                flash(beer)
        return redirect(url_for('review'))
    return render_template(url_for('review'), title='Check a Review', form=form)

@app.route('/base.html')
def base():
    return render_template(url_for('base'), title='Base')
