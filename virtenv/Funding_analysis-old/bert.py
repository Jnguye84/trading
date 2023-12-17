from transformers import BertTokenizerFast, BertForSequenceClassification
from transformers import pipeline


finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizerFast.from_pretrained('yiyanghkust/finbert-tone')

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

def sentiment(textlist):
    return nlp(textlist)


# sentences = ["Contact PR Newswire         Call 888-776-0942 from 8 AM - 9 PM ET   Chat with an Expert       Contact Us    General Inquiries    Request a Demo    Editorial Bureaus    Partnerships    Media Inquiries    Worldwide Offices                  Products     For Marketers    For Public Relations    For IR & Compliance    For Agency    For Small Business    All Products          About     About PR Newswire    About Cision    Become a Publishing Partner    Become a Channel Partner    Careers    Accessibility Statement      Global Sites    Asia    Brazil    Canada    Czech    Denmark    Finland    France    Germany    India    Israel    Italy    Mexico    Middle East    Middle East - Arabic    Netherlands    Norway    Poland    Portugal    Russia    Slovakia    Spain    Sweden    United Kingdom              My Services     All New Releases    Online Member Center    ProfNet         Contact Cision    Products    About     My Services   All News Releases   Online Member Center   ProfNet       Cision Distribution Helpline 888-776-0942            Terms of Use  Privacy Policy  Information Security Policy  Site Map  RSS  Cookie Settings     Copyright © 2023 Cision US Inc. "]

# print(sentiment(sentences))
# print(results)  #LABEL_0: neutral; LABEL_1: positive; LABEL_2: negative
