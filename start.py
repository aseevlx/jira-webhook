# -*- coding: utf-8 -*-
from flask import Flask, request, make_response
from datetime import datetime, date
from docxtpl import DocxTemplate

import json
from pprint import pprint
import traceback

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hook():
	if request.method == 'POST':
		
		data = request.data
		data = data.decode('utf-8')
	
		def string_to_date(datestring):
			"""Convert string with date from Jira to Python date type"""
			return datetime.strptime(datestring, '%Y-%m-%d')

		def holiday_duration(start_of_holiday, end_of_holiday):
			"""Calculate duration of holiday"""
			return str(string_to_date(end_of_holiday) - string_to_date(start_of_holiday)).split()[0]

		try:
			jdata = json.loads(data)

			if jdata['webhookEvent'] == 'jira:issue_created' or jdata['webhookEvent'] == 'jira:issue_updated':

				start_of_holiday = jdata['issue']['fields']['customfield_16600']
				end_of_holiday = jdata['issue']['fields']['customfield_16601']

				str_to_doc = {'reporter_name': jdata['issue']['fields']['customfield_17600'],
							'office_position': jdata['issue']['fields']['customfield_17601'],
							'reporter_name': jdata['issue']['fields']['customfield_17600'],
							'issue_type': jdata['issue']['fields']['issuetype']['name'],
							'start_day': start_of_holiday.split('-')[2],
							'start_month': start_of_holiday.split('-')[1],
							'end_day': end_of_holiday.split('-')[2],
							'end_month': start_of_holiday.split('-')[1],
							'end_year': start_of_holiday.split('-')[0],
							'end_of_holiday': jdata['issue']['fields']['customfield_16601'],
							'holiday_duration': holiday_duration(start_of_holiday, end_of_holiday),
							'now_day': date.today().isoformat().split('-')[2],
							'now_month': date.today().isoformat().split('-')[1],
							'now_year': date.today().isoformat().split('-')[0]}

				doc = DocxTemplate("template_opl.docx")
				doc.render(str_to_doc)
				doc.save(jdata['issue']['key'] + ".docx")

				ticket_key = jdata['issue']['key']
				reporter_name = jdata['issue']['fields']['reporter']['displayName']
				issue_type = jdata['issue']['fields']['issuetype']['name']
				holiday_duration = holiday_duration(start_of_holiday, end_of_holiday)

#				print('Ticket: %s | Reporter: %s' % (ticket_key, str_to_doc['reporter_name']))
#				print('Issue type is: %s' % str_to_doc['issue_type'])
#				print('Начало отпуска: %s, конец отпуска: %s, отпуск длится: %s' % (str_to_doc['start_of_holiday'], str_to_doc['end_of_holiday'], str_to_doc['holiday_duration']))
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
	return "Jira webhook listener"

if __name__ == '__main__':
	app.run(host='127.0.0.1',
		debug=True)
