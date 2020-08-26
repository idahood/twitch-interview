import json
import os
import requests
from flask import Flask, Markup, abort, render_template

'''
Background:

Your CEO has asked you to produce a report showing all our public peering exchange points for AS46489 and create an executive summary for him.

Requirements:

Please write an application using peeringdb API (https://peeringdb.com/apidocs/)
Your CEO would like to see a list of all the public peerings grouped by peering exchange point name.
He would also like an executive summary showing total peerings, total unique organization peerings, and total aggregate speed.

The CEO is known for being impressed if any other useful information is also shown in the executive summary.

Bonus:

If possible create a database backed web application to display the data.
If possible provide automated testing for your code.
If possible put the app on AWS or favorite cloud service.
'''

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Not dead yet</h1>"

@app.route('/<int:asn>')
def report(asn):
    response = requests.get(f'https://peeringdb.com/api/net?asn={asn}&depth=2')

    if response.status_code == 200:
        asn_net = json.loads(response.text)

        ix_aggregate = {}
        total_aggregate_speed = 0
        ix_ids = []

        for item in asn_net['data'][0]['netixlan_set']:
            ix_ids.append(item['ix_id'])
            ix = item['name']
            speed = item['speed']
            total_aggregate_speed += speed
            if ix in ix_aggregate:
                ix_aggregate[ix] += speed
            else:
                ix_aggregate[ix] = speed

        my_asns = set()
        for item in ix_ids:
            r = requests.get(f'https://peeringdb.com/api/ixlan?ix_id={item}&depth=2')
            ix_info = json.loads(r.text)
            for network in ix_info['data'][0]['net_set']:
                my_asns.add(network['asn'])

        return render_template('report.html', ix_aggregate=ix_aggregate, asn=asn,
                               total_bw=total_aggregate_speed,
                               total_peers=len(ixs['data'][0]['netixlan_set']),
                               unique_peers=len(ix_aggregate),
                               my_asns=my_asns)

    else:
        abort(response.status_code)

if __name__ == '__main__':
    app.run()
