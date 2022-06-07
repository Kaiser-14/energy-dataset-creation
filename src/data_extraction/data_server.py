import requests
import json
import time
import datetime

# Request API data and save into file

while True:
	# Get data from server
	server_request = requests.get('http://localhost:5000/api/probe')
	timestamp = datetime.datetime.now().timestamp()

	# Jsonify data
	data = json.loads(server_request.content)
	data.append({'timestamp': timestamp})
	data_json = json.dumps(data)

	# Save data into file
	with open('server.txt', 'a') as file:
		file.write(data_json)
		file.write('\n')

	# Wait until every metric is pushed into the server from probe
	time.sleep(15)
