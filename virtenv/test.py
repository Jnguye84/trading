import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
import rpy2.robjects as robjects
from rpy2.robjects import conversion, default_converter

def reddit():
    with conversion.localconverter(default_converter):
        r = robjects.r
        r['source']('virtenv/data.R')  
    with localconverter(ro.default_converter + pandas2ri.converter):
        results_reddit = robjects.r['reddit']
        results_reddit()
    return 'Uploaded BarPlot!'

reddit()