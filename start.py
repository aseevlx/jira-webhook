# -*- coding: utf-8 -*-
from flask import Flask, request
import json
import traceback

app = Flask(__name__)

CERT_KEY = ('/var/www/httpd-cert/aseev/easr.ru_le1.key')
CERT = ('/var/www/httpd-cert/aseev/easr.ru_le1.crt')
context = (CERT, CERT_KEY)

@app.route('/', methods=['POST'])
def hook():
	if request.method == 'POST':
		print('Сейчас произошел POST-запрос')

		data = request.data
		try:
			jdata = json.loads(data)

			if jdata['webhookEvent'] == 'jira:issue_created':
				ticket_key = jdata['issue']['key']

				print('Ticket: %s | %s' % (ticket_key, ticket_summary))
				return make_response('ok', 200)
			else:
				msg = 'Invalid JIRA hook event. It should be "jira:issue_created"'
				print(msg)
				return make_response(msg, 403)

		except:
			print(traceback.format_exc())
			msg = 'Incorrect data! Can not parse to json format'
			print(msg)
			return make_response(msg, 500)

@app.route('/', methods=['GET'])
def index():
	return make_response("Jira webhook")

if __name__ == '__main__':
	app.run(host='0.0.0.0',
		ssl_context=context,
		debug=True)
