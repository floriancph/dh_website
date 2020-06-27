from influxdb import InfluxDBClient
import requests, json
import pandas as pd
import datetime as dt
from webapp.get_key import get_secret

database = 'test'

def testings():
    sec = get_secret('influxdb')
    return sec['user']