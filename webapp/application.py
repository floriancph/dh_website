#!flask/bin/python
import json
from flask import Flask, Response, render_template
from webapp.flaskrun import flaskrun
from webapp.db_wrapper import getTopThreeNews, getTotalNewsResults

application = Flask(__name__)

@application.route('/', methods=['GET'])
def index():
    top_three_news = getTopThreeNews() # Get Top Three Trends
    total_news_results = getTotalNewsResults() # Get Total Number of News Articles (in order to calculate percentage)
    return render_template('index.html', top_three_news=top_three_news, total_news_results=total_news_results)

@application.route('/test', methods=['GET'])
def test():
    # pas = get_key.get_secret("influxdb")
    return Response(json.dumps({'Output': 'Moinsen'}), mimetype='application/json', status=200)

if __name__ == '__main__':
    flaskrun(application)
