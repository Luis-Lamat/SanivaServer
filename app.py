import requests
from flask import Flask, url_for, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome. Send a request to `/machine_info.json` to get a json response'

@app.route('/machine_info.json')
def api_machine_info():
	# Getting the whole html from the page
	response = requests.get('http://95.209.150.208/eng/Status.asp')

	# Making a parse tree from that plain html for element lookup
	soup = BeautifulSoup(response.text, 'html.parser')

	# Getting the second table that holds the info
	table = soup.find_all('table')[1]

	# Getting the table data through its usless noborder class
	table = [x.text for x in table.select('.noborder')]
	labels = ['WASH_' + str(i) for i in xrange(3)] + ['DRY_' + str(i) for i in xrange(3)]
	statuses = [table[i] for i in (2,7,12,17,22,27)]
	data = dict(zip(labels, statuses))
	resp = jsonify(data)
	resp.status_code = 200
	return resp

if __name__ == '__main__':
    app.run()

