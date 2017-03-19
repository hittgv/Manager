import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


def scoreArticle(df, model):

    print "scoring model"

    # Drop URL in order to allow the cast to numeric to *not* fail
    df = df.drop('url', 1)

    probs = model.predict_proba(df)
    print probs

    probability_of_fake = probs[0][0]*100

    # Probability of FAKE NEWS is first in the array (element 0)
    # return probs

    print probability_of_fake

    return int(probability_of_fake)
