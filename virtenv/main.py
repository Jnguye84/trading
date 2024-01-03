from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from flask import Flask, render_template, url_for, redirect, request, session
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
    psize = IntegerField('Portfolio Size', validators=[InputRequired()])
    company = StringField('Company', validators=[InputRequired()])
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
    return results_sentiment

def results_participants(drug):
    with conversion.localconverter(default_converter):
        r = robjects.r
        r['source']('virtenv/data.R')  
    with localconverter(ro.default_converter + pandas2ri.converter):
        drug_r = ro.conversion.py2rpy(drug)
    results_participants = robjects.r['results_participants']
    results_participants_r = results_participants(drug_r)
    with localconverter(ro.default_converter + pandas2ri.converter):
        results_participants = ro.conversion.py2rpy(results_participants_r)
    return results_participants

def reddit():
    with conversion.localconverter(default_converter):
        r = robjects.r
        r['source']('virtenv/data.R')  
    with localconverter(ro.default_converter + pandas2ri.converter):
        results_reddit = robjects.r['reddit']
        results_reddit_r = results_reddit()
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    with localconverter(ro.default_converter + pandas2ri.converter):
        results_reddit = ro.conversion.py2rpy(results_reddit_r)
        results_reddit = ro.conversion.rpy2py(results_reddit)
    return results_reddit 

def reddit_csv(drug, company):
    with conversion.localconverter(default_converter):
        r = robjects.r
        r['source']('virtenv/reddit.R')  
    with localconverter(ro.default_converter + pandas2ri.converter):
        drug_r = ro.conversion.py2rpy(drug)
        company_r = ro.conversion.py2rpy(company)
    results_reddit_csv = robjects.r['reddit_csv']
    results_reddit_csv(drug_r, company_r)
    #ro.conversion.rpy2py(function) making things into a dataframe
    return 'Finished Running Monthly Reddit CSV File!'

#subprocess.run(['python', 'k_means.py'])

@APP.route('/', methods=['GET', 'POST'])
def home():
    form = FillinFields()
    if form.validate_on_submit():
        drug = form.drug.data
        psize = form.psize.data
        company = form.company.data

        session['drug'] = drug
        session['psize'] = psize
        session['company'] = company

        return redirect(url_for('results'))
    return render_template('index.html', form=form)

@APP.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        drug = session.get('drug')
        psize = session.get('psize')
        company = session.get('company')
        reddit_csv(drug, company) #running the reddit csv (once per month)
        #running finbert sentiment for specific ticker
        if 'Results Sentiment' in request.form:
            results_sentiments = results_sentiment(drug)
            return render_template('sentiments.html', results_sentiment=results_sentiments)
        elif 'Results Participants' in request.form:
            results_participant = results_participants(drug)
            return render_template('participants.html', results_participants=results_participant)
        elif 'Results Reddit' in request.form:
            reddit()
            return render_template('reddit.html')
        elif 'Results K-Means Fin Bert' in request.form:
            kmeans = kmeans(drug, company)
        return render_template('drug.html', )
    return render_template('drug.html')

APP.run()

