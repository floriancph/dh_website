from influxdb import InfluxDBClient
import requests, json
import pandas as pd
import datetime as dt
from webapp.get_key import get_secret

database = 'test'

##### OVERARCHING FUNCITONS #####

def sortTrends(trends, attribute):
    return sorted(trends, key = lambda i: i[attribute],reverse=True)

def formatQueryResult(query_result):
    query_result = list(query_result)
    for line in query_result[0]:
        line['twitter_hashtags'] = line['twitter_hashtags'].replace("[", "")
        line['twitter_hashtags'] = line['twitter_hashtags'].replace("]", "")
        line['twitter_hashtags'] = line['twitter_hashtags'].replace("'", "")
        line['twitter_hashtags'] = line['twitter_hashtags'].replace(" ", "")
        line['twitter_hashtags'] = line['twitter_hashtags'].split(',')

        line['influencial_tweets'] = line['influencial_tweets'].replace("[", "")
        line['influencial_tweets'] = line['influencial_tweets'].replace("]", "")
        line['influencial_tweets'] = line['influencial_tweets'].replace("'", "")
        line['influencial_tweets'] = line['influencial_tweets'].replace(" ", "")
        line['influencial_tweets'] = line['influencial_tweets'].split(',')
    return query_result[0]

def checkIfDouble(query_result):
    trends = [] # Return object
    trends_added = [] # List of trend titles added
    for line in query_result:
        trend = line['trend']
        if trend not in trends_added: # check if trend already added
            trends.append(line) # add dataset to result
            trends_added.append(trend) # add title of trend to trends added
    return trends

##### SOCIAL PAGE ###### 

def getSocial():
    sec = get_secret('influxdb')
    try:
        client = InfluxDBClient(host=sec['host'], port=int(sec['port']), username=sec['user'], password=sec['pw'], ssl=False, verify_ssl=False)
        result = client.query("SELECT * FROM social WHERE time > (now() - 120m)", database=database)
    except:
        result = []
    
    if len(result) > 0:
        result = formatQueryResult(result)
        result = checkIfDouble(result)
        result = sortTrends(result, 'number_of_articles')
    
    return result

###### LANDING PAGE ######

def getTotalNewsResults():
    trends = getSocial()
    total_number = 0
    for i in trends:
        total_number = total_number + i['number_of_articles']
    return total_number

def getTopThreeNews():
    trends = getSocial()
    top_three_trends = sortTrends(trends, 'number_of_articles')
    return top_three_trends[:3]