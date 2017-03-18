from lxml import html
import requests
from flask import Flask
from flask import request
import json

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

    alexa = collectAlexaFeatures("http://localhost:3000", payload, headers)

    print alexa

    # Score page based on features
    
    score = 9

    return json.dumps({"assignedScore":score})

if __name__ == "__main__":
    app.run(debug=True)
    # title = tree.xpath('//title/text()')
    # header = tree.xpath('//h1/text()')