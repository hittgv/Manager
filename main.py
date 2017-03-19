import json
from multiprocessing import Pool

import numpy as np
import pandas as pd
import requests
import sklearn
from flask import Flask, request
from lxml import html

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
    features = []

    # alexa data frame
    alexa = collectAlexaFeatures("http://localhost:3000", payload, headers)
    ads = collectAdsFeatures("http://localhost:3000", payload, headers)

    features.append(alexa)
    features.append(ads)
    feature_frame = pd.DataFrame({'url':payload['url']}, index=[0])

    for i in range(len(features)):
        # print feature_frame
        # print features[i]
        # print "---------"
        feature_frame.merge(alexa, how='outer',left_on='url', right_on='url')

    print(feature_frame)
    print(alexa)

    #join all data frames together, using URL as the key (or just colbind...)

    # put data through predefined scorecard
    
    score = 9

    return json.dumps({"assignedScore":score})

if __name__ == "__main__":
    app.run(debug=True)
    # title = tree.xpath('//title/text()')
    # header = tree.xpath('//h1/text()')
