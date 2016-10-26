# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, jsonify
import json
import traceback

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hook():
	if request.method == 'POST':
		print('Сейчас произошел POST-запрос')
		data = request.data
		data = data.decode('utf-8')

		try:
			jdata = json.loads(data)

			if jdata['webhookEvent'] == 'jira:issue_created' or jdata['webhookEvent'] == 'jira:issue_updated':
				ticket_key = jdata['issue']['key']

				print('Ticket: %s' % (ticket_key))
				print(jdata)
				return make_response('ok', 200)
			else:
				msg = 'Invalid JIRA hook event. It should be "jira:issue_created" or "_updated"'
				print(msg)
				return make_response(msg, 403)

		except:
			print(traceback.format_exc())
			msg = 'Incorrect data! Can not parse to json format'
			print(msg)
			return make_response(msg, 500)

@app.route('/', methods=['GET'])
def index():
	return "Jira webhook"

if __name__ == '__main__':
	app.run(host='127.0.0.1',
		debug=True)
