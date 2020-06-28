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

##### HASHTAG PAGE ######

def getHashtagResults(twitter_hashtag):
    sec = get_secret('influxdb')
    try:
        client = InfluxDBClient(host=sec['host'], port=int(sec['port']), username=sec['user'], password=sec['pw'], ssl=False, verify_ssl=False)
        result = client.query("SELECT * FROM social", database=database)
        result = formatQueryResult(result)
    except:
        result = []
    
    list_of_trends = []
    for element in result:
        if twitter_hashtag in element['twitter_hashtags']:
            list_of_trends.append(element)

    # Summarize list_of_trends
    trends_consolidated = {} # Dict der konsolidierten Trends zum Hashtag
    hashtags_consolidated = {} # TODO hashtags_consolidated = {} # Dict der konsolidierten Hashtags zum Hashtag 
    data = []  # Liste der Datum an denen der Hashtag vorkommt
    columns = ['date'] # Spaltenebezeichnung im Pandas DataFrame

    for trend in list_of_trends:
        # Füge die Trend-Bezeichnung in die konsolidierte Liste hinzu
        if trend['trend'].upper() in trends_consolidated: 
            trends_consolidated[trend['trend'].upper()] += 1
        else:
            trends_consolidated[trend['trend'].upper()] = 1
        
        if trend['trend'].upper() not in hashtags_consolidated:
            hashtags_consolidated[trend['trend'].upper()] = {}
        for hashtag in trend['twitter_hashtags']:
            if hashtag in hashtags_consolidated[trend['trend'].upper()]:
                hashtags_consolidated[trend['trend'].upper()][hashtag] += 1
            else:
                hashtags_consolidated[trend['trend'].upper()][hashtag] = 1

        date = trend['time'][:10] # Hole Datum aus Trend heraus
        data.append(date) # Füge das Datum der Liste hinzu

    # sort dict:
    trends_consolidated = {k: v for k, v in sorted(trends_consolidated.items(), key=lambda item: item[1], reverse=True)}
    for trend in list(hashtags_consolidated.keys()):
        rearrange = hashtags_consolidated[trend]
        rearrange = {k: v for k, v in sorted(rearrange.items(), key=lambda item: item[1], reverse=True)}
        hashtags_consolidated[trend] = list(rearrange.keys())

    df = pd.DataFrame(data, columns=columns)
    df['count'] = 1
    summen = df.groupby(['date'], as_index = False).sum()
    datum = summen['date'].values.tolist()
    werte = summen['count'].values.tolist()
    return [list(trends_consolidated.keys()), datum, werte, hashtags_consolidated]


###### KNOWLEDGE GRAPH ####

def KnowledgeGraph():
    sec = get_secret('influxdb')
    try:
        client = InfluxDBClient(host=sec['host'], port=int(sec['port']), username=sec['user'], password=sec['pw'], ssl=False, verify_ssl=False)
        result = client.query("SELECT * FROM social WHERE time > (now() - 120m)", database=database)
    except:
        result = []
        
    if len(result) > 0:
        result = formatQueryResult(result)
        send = {"data": result}
        r = requests.post('https://04cdmjq6ga.execute-api.eu-central-1.amazonaws.com/default/KnowledgeGraph', data=json.dumps(send))
        return json.loads(r.text)
    else:
        return 0