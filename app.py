import json
import requests
from flask import Flask, Markup, abort, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>https://twitch-interview.herokuapp.com/ASN</h1>"

@app.route('/<int:asn>')
def report(asn):
    response = requests.get(f'https://peeringdb.com/api/net?asn={asn}&depth=2')

    if response.status_code == 200:
        ixs = json.loads(response.text)

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

        return render_template('report.html', ix_aggregate=ix_aggregate, asn=asn,
                               total_bw=total_aggregate_speed,
                               total_peers=len(ixs['data'][0]['netixlan_set']),
                               unique_peers=len(ix_aggregate))
    else:
        abort(response.status_code)

if __name__ == '__main__':
    app.run()
