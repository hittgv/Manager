from lxml import html
import requests
from flask import Flask
from flask import request
import json
import pandas as pd
import numpy as np
# user defined functions
from functions import *
from scoreout import *

app = Flask(__name__)

ADCOUNT = "https://adshunter.herokuapp.com"
ALEXA = "https://alexar.herokuapp.com"
DEADLINKS = "https://broken-links-service.herokuapp.com/"
SELFLINKS = 'https://self-link-service.herokuapp.com/'


@app.route("/", methods=['POST'])
def hello():
    url = json.loads(request.data)['url']
    page = requests.get(url)
    payload = {
        "html": page.text,
        "url": str(url)
        }
    headers = {"Content-Type": "application/json"}

    brokenlinks = collectBrokenLinks(DEADLINKS, payload, headers)
    alexa = collectAlexaFeatures(ALEXA, payload, headers)
    selflinks = collectSelflinks(SELFLINKS, payload, headers)


    # join all data frames together, using URL as the key (or just colbind...)
    all_features = brokenlinks.merge(alexa, how='inner', on='url').merge(selflinks, how='inner', on='url')

    score = int(scoreArticle(all_features))

    print(score)

    return json.dumps({"assignedScore": score})


@app.route("/train", methods=['POST'])
def train():
    url = json.loads(request.data)['url']
    page = requests.get(url)
    payload = {
        "html": page.text,
        "url": str(url)
        }
    headers = {"Content-Type": "application/json"}


    selflinks = collectSelflinks(SELFLINKS, payload, headers)
    brokenlinks = collectBrokenLinks(DEADLINKS, payload, headers)
    alexa = collectAlexaFeatures(ALEXA, payload, headers)


    # could use pd.concat() to make this cleaner later.
    all_features = brokenlinks.merge(alexa, how='inner', on='url').merge(selflinks, how='inner', on='url')

    return all_features.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
