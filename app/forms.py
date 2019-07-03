from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
    beer_review = StringField('Beer Review', validators=[DataRequired()])
    submit = SubmitField('Submit')
