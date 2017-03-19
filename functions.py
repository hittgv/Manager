from lxml import html
import requests
from flask import Flask
from flask import request
import json
import numpy as np
import pandas as pd



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
    alexa_dict = {'url': payload['url'], 'dailyTimeOnSite': alexa_engagement['dailyTimeOnSite'], 'bounceRate': alexa_engagement['bounceRate'], 'dailyPageViewPerVisitor': alexa_engagement['dailyPageViewPerVisitor'], 'globalRank': alexa_globalRank}
    alexa_df = pd.DataFrame(alexa_dict, index=[0])

    # return the dataframe
    return alexa_df


def collectNumberOfAdverts(featureUrl, payload, headers):
    r = requests.post(
        featureUrl,
        data=json.dumps(payload),
        headers=headers
        )
    ads = json.loads(str(r.text))
    ads_dict = {'url': payload['url'], "numberOfAds": len(ads['crawl']['ads'])}
    ads_pagestats = ads['psi']['pageStats']

    for key, value in ads_pagestats.iteritems():
        ads_dict[key] = value
    ads_df = pd.DataFrame(ads_dict, index=[0])

    return ads_df


def collectBrokenLinks(featureUrl, payload, headers):
    r = requests.post(
        featureUrl,
        data=json.dumps(payload),
        headers=headers
        )

    deadLinks = json.loads(str(r.text))
    deadLinks_dict = {'url': payload['url'],'goodOutLinks': deadLinks['SUCCESS'], 'badOutLinks': deadLinks['FAIL'], 'redirectOutLinks': deadLinks['REDIRECT']}
    deadLinks_df = pd.DataFrame(deadLinks_dict, index=[0])

    return deadLinks_df

def collectSelflinks(featureUrl, payload, headers):
    r = requests.post(
        featureUrl,
        data=json.dumps(payload),
        headers=headers
        )
    selfLinks = json.loads(str(r.text))
    selfLinks_dict = {'url': payload['url'], 'internalLinks': selfLinks['internalLinks'], 'outboundLinks': selfLinks['externalLinks']}
    selfLinks_df = pd.DataFrame(selfLinks_dict, index=[0])

    return selfLinks_df
