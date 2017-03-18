from lxml import html
import requests
from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route("/", methods = ['POST'])
def hello():
    url =  json.loads(request.data)['url']
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # DO ALL MY FEATURE GENERATION STUFF
    # Call Dave's service
    # give him page.text

    # Score page based on features
    
    score = 9

    return json.dumps({"assignedScore":score})

if __name__ == "__main__":
    app.run()



    
    # title = tree.xpath('//title/text()')

    # header = tree.xpath('//h1/text()')
