#!flask/bin/python
import json
from flask import Flask, Response, render_template
from webapp.flaskrun import flaskrun
from webapp.db_wrapper import getTopThreeNews, getTotalNewsResults, getSocial, getHashtagResults, KnowledgeGraph

application = Flask(__name__, static_url_path='/static')

@application.route('/', methods=['GET'])
def index():
    top_three_news = getTopThreeNews() # Get Top Three Trends
    total_news_results = getTotalNewsResults() # Get Total Number of News Articles (in order to calculate percentage)
    return render_template('index.html', top_three_news=top_three_news, total_news_results=total_news_results)

@application.route('/social', methods=['GET'])
def social():
    db_result = getSocial() # Get latest Trends (db-write within last 60mins. & sorted by no. of articles)
    x_values = []
    y_values = []

    if len(db_result) > 0:
        for trend in db_result:
            x_values.append(trend['number_of_articles'])
            y_values.append(trend['trend'])

    return render_template('social.html', db_result=db_result, x_values=x_values, y_values=y_values)

@application.route('/hashtag/<hashtag>', methods=['GET'])
def byHashtag(hashtag):
    hashtag = hashtag.lower()
    db_result = getHashtagResults(hashtag)
    list_of_trends = db_result[0]
    datum = json.dumps(db_result[1])
    werte = db_result[2]
    hashtags = db_result[3]
    return render_template('hashtag.html', list_of_trends=list_of_trends, hashtag=hashtag, datum=datum, werte=werte, hashtags=hashtags)

@application.route('/graph', methods=['GET'])
def graph():
    result = KnowledgeGraph()
    if result != 0:
        return render_template('force.html', result=result)
    else:
        return render_template('error.html')

@application.route('/getMyJson')
def getMyJson():
    result = KnowledgeGraph()
    response = Response(response=json.dumps(result), status=200, mimetype="application/json")
    return(response)

######## ERROR HANDLING ########

@application.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@application.errorhandler(505)
def internal_server_error(e):
    return render_template('error.html'), 505

if __name__ == '__main__':
    flaskrun(application)