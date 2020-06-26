#!flask/bin/python
import json
from flask import Flask, Response, render_template
from webapp.flaskrun import flaskrun

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return render_template('index.html', top_three_news=[], total_news_results=[])
    # return Response(json.dumps({'Output': 'Moin!!'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Moin'}), mimetype='application/json', status=200)

if __name__ == '__main__':
    flaskrun(application)
