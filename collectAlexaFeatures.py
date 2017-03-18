from lxml import html
import requests
from flask import Flask
from flask import request
import json


def collectAlexaFeatures(featureUrl, payload, headers):
    r = requests.post(featureUrl,data=json.dumps(payload), headers=headers)
    alexa =  json.loads(str(r.text))
    return alexa