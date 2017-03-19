from lxml import html
import requests
from flask import Flask
from flask import request
import json
import pandas as pd
import numpy as np
# user defined functions
from functions import *

app = Flask(__name__)


@app.route("/", methods = ['POST'])
def hello():
    url =  json.loads(request.data)['url']
    page = requests.get(url)
    tree = html.fromstring(page.content)
    payload = {
#        "HTML":page.text,
        "url":str(url)
        }

    headers = {"Content-Type":"application/json"}

    # alexa data frame
    alexa = collectAlexaFeatures("http://localhost:3000", payload, headers)

    #join all data frames together, using URL as the key (or just colbind...)

    # put data through predefined scorecard
    
    score = 9

    return json.dumps({"assignedScore":score})

if __name__ == "__main__":
    app.run(debug=True)
    # title = tree.xpath('//title/text()')
    # header = tree.xpath('//h1/text()')