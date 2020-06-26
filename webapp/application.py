#!flask/bin/python
import json
from flask import Flask, Response, render_template
from webapp.flaskrun import flaskrun
import webapp.get_key as get_key

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    pas = get_key.get_secret("influxdb")
    return render_template('index.html', top_three_news=[], total_news_results=[], user=pas['user'])
    # return Response(json.dumps({'Output': 'Moin!!'}), mimetype='application/json', status=200)

@application.route('/test', methods=['GET'])
def test():
    # pas = get_key.get_secret("influxdb")
    return Response(json.dumps({'Output': 'Moin'}), mimetype='application/json', status=200)

if __name__ == '__main__':
    flaskrun(application)
