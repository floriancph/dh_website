from influxdb import InfluxDBClient
import requests, json
import pandas as pd
import datetime as dt
from webapp.get_key import get_secret

database = 'test'

def testings():
    sec = get_secret('influxdb')
    client = InfluxDBClient(host='ec2-3-122-193-51.eu-central-1.compute.amazonaws.com', port=int(sec['port']), username=sec['user'], password=sec['pw'], ssl=False, verify_ssl=False)
    result = client.query("SELECT * FROM social WHERE time > (now() - 120m)", database=database)
    return (sec['user'], len(result))