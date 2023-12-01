#finding SA for first 50 articles in alpha vantage API based on ticker
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import nltk
from bert import sentiment
import requests
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import pandas as pd
import matplotlib.pyplot as plt
nltk.download('punkt')


