from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from flask import Flask, render_template
import pandas as pd
from wtforms.validators import InputRequired
#pip install rpy2==3.5.1
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as robjects
from rpy2.robjects import conversion, default_converter

APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'secretkey'

class FillinFields(FlaskForm):
    drug = StringField('Drug Name', validators=[InputRequired()])
    psize = StringField('Portfolio Size')
    submit = SubmitField('Submit')

def results_sentiment(drug):
    with conversion.localconverter(default_converter):
        r = robjects.r
        r['source']('virtenv/data.R')  
    with localconverter(ro.default_converter + pandas2ri.converter):
        drug_r = ro.conversion.py2rpy(drug)
    results_sentiment = robjects.r['results_sentiment']
    results_sentiment_r = results_sentiment(drug_r)
    with localconverter(ro.default_converter + pandas2ri.converter):
        results_sentiment = ro.conversion.py2rpy(results_sentiment_r)
        results_sentiment = ro.conversion.rpy2py(results_sentiment)
    return results_sentiment

@APP.route('/', methods=['GET', 'POST'])
def home():
    form = FillinFields()
    if form.validate_on_submit():
        drug = form.drug.data
        psize = form.psize.data
        results_sentiments = results_sentiment(drug)
        return render_template('drug.html', drug=drug, psize=psize, results_sentiment=results_sentiments.to_html())
    return render_template('index.html', form=form)

APP.run()
# Defining the R script and loading the instance in Python

# Loading the function we have defined in R.

