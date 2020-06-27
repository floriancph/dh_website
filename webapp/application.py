#!flask/bin/python
import json
from flask import Flask, Response, render_template
from webapp.flaskrun import flaskrun
from webapp.db_wrapper import getTopThreeNews, getTotalNewsResults, getSocial

application = Flask(__name__)

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

if __name__ == '__main__':
    flaskrun(application)
