#!/usr/bin/env python3

import json
import requests
from flask import Flask, Markup, render_template

'''
Background:

Your CEO has asked you to produce a report showing all our public peering exchange points for AS46489 and create an executive summary for him.

Requirements:

Please write an application using peeringdb API(https://peeringdb.com/apidocs/).
Your CEO would like to see a list of all the public peerings grouped by peering exchange point name.
He would also like an executive summary showing total peerings, total unique organization peerings, and total aggregate speed.

The CEO is known for being impressed if any other useful information is also shown in the executive summary.

Bonus:

If possible create a database backed web application to display the data.
If possible provide automated testing for your code.
If possible put the app on AWS or favorite cloud service.
'''

app = Flask(__name__)

@app.route('/<int:asn>')
def report(asn):
    r = requests.get(f'https://peeringdb.com/api/net?asn={asn}&depth=2')
    ixs = json.loads(r.text)

    ix_aggregate = {}
    total_aggregate_speed = 0

    for item in ixs['data'][0]['netixlan_set']:
        ix = item['name']
        speed = item['speed']

        total_aggregate_speed += speed

        if ix in ix_aggregate:
            ix_aggregate[ix] += speed
        else:
            ix_aggregate[ix] = speed

    return render_template('report.html', title='Peering Bandwith per IX', ix_aggregate=ix_aggregate, asn=asn,
                           total_bw=total_aggregate_speed, total_peers=len(ixs['data'][0]['netixlan_set']),
                           unique_peers=len(ix_aggregate))

def main():
    app.debug = True
    app.run(host='0.0.0.0', port=80)

main()
