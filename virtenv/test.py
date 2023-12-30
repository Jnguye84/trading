import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as robjects
import pandas as pd
import rpy2.robjects as ro
import tabulate

r = robjects.r
r['source']('virtenv/data.R')
drug = 'Exparel'

with localconverter(ro.default_converter + pandas2ri.converter):
    drug_r = ro.conversion.py2rpy(drug)
results_sentiment = robjects.r['results_sentiment']
results_sentiment_r = results_sentiment(drug_r)

with localconverter(ro.default_converter + pandas2ri.converter):
    results_sentiment = ro.conversion.py2rpy(results_sentiment_r)
    results_sentiment = ro.conversion.rpy2py(results_sentiment)

print(tabulate(results_sentiment, headers='keys', tablefmt='psql'))
#[['title', 'description', 'nct_id', 'non_inferiority_desc', 'p_value']]