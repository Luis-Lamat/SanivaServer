import requests
import time
from logger import *
from flask import Flask, url_for, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

FIVE_MINUTES = 420
time1 = time.time()
time2 = time.time()
resp = None

dorms = {
	0: '95.209.150.208', # Kathrine Kollegiet
	1: '77.75.166.66',	 # Porcelaenshaven
	2: '95.209.150.175'  # Holger Danske
}

@app.route('/')
def api_root():
    return '''
    	<h1>Welcome</h1>
    	Send a request to <code>`/machine_info.json`</code> to get a json 
    	response of the machine statuses. <br>
    	Send dorm number as a param called <code>`dorm`</code> to select the 
    	dorm info (default is Kathrine Kollegiet). <br><br>
    	Dorm numbers:
		<ol>
			<li> Kathrine Kollegiet </li>
			<li> Porcelaenshaven </li>
			<li> Holger Danske </li>
		</ol>
		'''

@app.route('/machine_info.json')
def api_machine_info():
	# Return the same data for every 7 minute interval
	global resp, time1, time2
	if resp and time2 - time1 < FIVE_MINUTES:
		Logger.log_time_diff(time2 - time1)
		time2 = time.time()
		return resp

	# Reset times
	time1 = time2 = time.time()

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

