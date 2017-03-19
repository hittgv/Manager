from lxml import html
import requests
from flask import Flask
from flask import request
import json
import pandas as pd
import numpy as np
from sklearn.externals import joblib

# user defined functions
from functions import *
from scoreout import *

model = joblib.load('fakeNews.pkl')

app = Flask(__name__)

ADCOUNT = "https://adshunter.herokuapp.com"
ALEXA = "https://alexar.herokuapp.com"
DEADLINKS = "https://broken-links-service.herokuapp.com/"
SELFLINKS = 'https://self-link-service.herokuapp.com/'


@app.route("/", methods=['POST'])
def hello():
    url = json.loads(request.data)['url']

    print "post recieved for:"
    print url
    
    page = requests.get(url)
    payload_heavy = {
        "html": page.text,
        "url": str(url)
        }
    payload_light = {
        "url": str(url)
        }
    headers = {"Content-Type": "application/json"}

    print "sending first request"
    brokenlinks = collectBrokenLinks(DEADLINKS, payload_heavy, headers)
    print "broken links done"
    alexa = collectAlexaFeatures(ALEXA, payload_light, headers)
    print "alexa done"
    selflinks = collectSelflinks(SELFLINKS, payload_heavy, headers)
    print "self links done"

    all_features = brokenlinks.merge(alexa, how='inner', on='url').merge(selflinks, how='inner', on='url')

    score = scoreArticle(all_features, model)

    return json.dumps({"assignedScore": score})


@app.route("/train", methods=['POST'])
def train():
    url = json.loads(request.data)['url']
    page = requests.get(url)
    payload_heavy = {
        "html": page.text,
        "url": str(url)
        }
    payload_light = {
        "url": str(url)
        }
    headers = {"Content-Type": "application/json"}

    brokenlinks = collectBrokenLinks(DEADLINKS, payload_heavy, headers)
    alexa = collectAlexaFeatures(ALEXA, payload_light, headers)
    selflinks = collectSelflinks(SELFLINKS, payload_heavy, headers)

    all_features = brokenlinks.merge(alexa, how='inner', on='url').merge(selflinks, how='inner', on='url')

    return all_features.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
