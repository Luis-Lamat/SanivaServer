import requests
import time
from logger import *
from error import *
from flask import Flask, url_for, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

FIVE_MINUTES = 300
current_time = time.time()
resp = None

dorms_info = {
	'0': { # Kathrine Kollegiet
		'ip': '95.209.150.208',
		'data': None,
		'last_request': current_time},
	'1': { # Porcelaenshaven
		'ip': '77.75.166.66',
		'data': None,
		'last_request': current_time},
	'2': { # Holger Danske
		'ip': '95.209.150.175',
		'data': None,
		'last_request': current_time},
}

def parse_response(html):
	# Making a parse tree from that plain html for element lookup
	soup = BeautifulSoup(html.text, 'html.parser')

	# Getting the second table that holds the info
	table = soup.find_all('table')[1]

	# Getting the table data through its usless noborder class
	table = [x.text for x in table.select('.noborder')]

	# Creating the desired json response | TODO: Add danish
	washer_count = len([x for x in table if x.find('WASH') > 0])
	dryer_count = len([x for x in table if x.find('DRYER') > 0])

	# Getting index of busy machines
	busy_machines = [(i-2)/5 for i, x in enumerate(table) if x == 'Busy']
	busy_washers = [x for x in busy_machines if x < washer_count]
	busy_dryers = [x for x in busy_machines if x >= dryer_count]

	data = {
		'washers': {
			'count': washer_count,
			'busy': busy_washers,
		},
		'dryers': {
			'count': dryer_count,
			'busy': busy_dryers,
		},
	}
	return jsonify(data)

def get_info(ip_address):
	# Getting the whole html from selected the page
	try:
		response = requests.get('http://' + ip_address + '/eng/Status.asp')
	except:
		return Error.gateway_timeout()
	return parse_response(response)

@app.route('/machine_info.json')
def api_machine_info():
	# Return the same data for every 7 minute interval
	global current_time
	dorm = '0' # Kathrine Kollegiet
	if 'dorm' in request.args:
		if request.args['dorm'] in dorms_info.keys():
			dorm = request.args['dorm']
		else:
			return Error.bad_request()

	last_request = dorms_info[dorm]['last_request']
	current_time = time.time()
	data = dorms_info[dorm]['data']
	if data and current_time - last_request < FIVE_MINUTES:
		Logger.log_time_diff(current_time - last_request)
		return data

	# Reset time
	dorms_info[dorm]['last_request'] = time.time()

	response = get_info(dorms_info[dorm]['ip'])
	response.status_code = 200
	dorms_info[dorm]['data'] = response
	return response

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

if __name__ == '__main__':
    app.run()

