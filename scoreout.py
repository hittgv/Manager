import pandas as pd
import numpy as np


def scoreArticle(df):

    # Drop URL in order to allow the cast to numeric to *not* fail
    df = df.drop('url', 1)

    # print "starting scoreout"
    # print(df)
    # print "---------------"
    # df.apply(pd.to_numeric)
    # print "---------------"
    # print(df)

    return df.sum(axis=1)%100