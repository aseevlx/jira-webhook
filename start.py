import json
from datetime import datetime

from flask import Flask, request, make_response
from docxtpl import DocxTemplate

app = Flask(__name__)


# TODO: change these fields to match your
custom_fields = {
	'start_of_vacation': 'customfield_16600',
	'end_of_vacation': 'customfield_16601',
	'reporter_name': 'customfield_17600',
	'office_position': 'customfield_17601',
}


@app.route('/', methods=['POST'])
def hook():
	try:
		payload = request.json
		supported_events = ('jira:issue_created', 'jira:issue_updated')

		if payload['webhookEvent'] not in supported_events:
			error_message = 'Invalid JIRA hook event. It should be "jira:issue_created" or "jira:issue_updated"'
			print(error_message)
			return make_response(error_message, 403)

		issue_fields = payload['issue']['fields']

		start_of_vacation = datetime.strptime(issue_fields[custom_fields['start_of_vacation']], '%Y-%m-%d')
		end_of_vacation = datetime.strptime(issue_fields[custom_fields['end_of_vacation']], '%Y-%m-%d')
		vacation_duration = (start_of_vacation - end_of_vacation).days

		doc_vars = {
			'reporter_name': issue_fields[custom_fields['reporter_name']],
			'office_position': issue_fields[custom_fields['office_position']],
			'issue_type': issue_fields['issuetype']['name'],
			'start_day': start_of_vacation.day,
			'start_month': start_of_vacation.month,
			'end_day': end_of_vacation.day,
			'end_month': end_of_vacation.month,
			'end_year': end_of_vacation.year,
			'end_of_vacation': end_of_vacation.strftime('%d-%m-%Y'),
			'vacation_duration': vacation_duration,
			'now_day': datetime.now().day,
			'now_month': datetime.now().month,
			'now_year': datetime.now().year,
		}

		ticket_key = payload['issue']['key']

		doc = DocxTemplate('template_opl.docx')
		doc.render(doc_vars)
		doc.save(ticket_key + '.docx')

		return make_response('ok', 200)

	except Exception as e:
		error_message = 'Incorrect data! Can\'t parse request: {}'.format(e)
		print(error_message)
		return make_response(error_message, 500)
