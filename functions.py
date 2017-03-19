import json

import numpy as np
import pandas as pd
import requests
import sklearn
from flask import Flask, request
from lxml import html


def collectAlexaFeatures(featureUrl, payload, headers):
    r = requests.post(
        featureUrl,
        data=json.dumps(payload),
        headers=headers
        )
    alexa = json.loads(str(r.text))

    alexa_engagement = alexa['engagement']
    alexa_countryRank = alexa['countryRank']
    alexa_globalRank = alexa['globalRank']

    # intentionally skipping countryrank for now
    alexa_dict = {'url':payload['url'],'dailyTimeOnSite': alexa_engagement['dailyTimeOnSite'],'bounceRate':alexa_engagement['bounceRate'],'dailyPageViewPerVisitor':alexa_engagement['dailyPageViewPerVisitor'],'globalRank': alexa_globalRank}
    alexa_df = pd.DataFrame(alexa_dict, index=[0])
    
    #return the dataframe
    return alexa_df

def collectAdsFeatures(featureUrl, payload, headers):
    r = requests.post(
        featureUrl,
        data=json.dumps(payload),
        headers=headers
        )
    ads = json.loads(str(r.text))

    return pd.DataFrame({'url':payload['url']}, index=[0])

    return ads
