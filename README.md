# jira_webhook
Small Python server, that listen for your Jira Webhooks and render .docx file.
Uses Python 3.5, Flask, and some other stuff.
Script generate new document from template_opl.docx and save new file with name "KEY-XX.docx" where "KEY" - key from task (JRA-1, for example)


Скрипт на Python, который слушает Jira Webhooks и генерирует .docx на основе данных из таска.
Используется для генерации заявления на отпуск, читает из полей "Начало отпуска", "Окончание отпуска", и т.д.
Итоговый документ генерируется с помощью jinja-templates из template_opl.docx и сохраняется с именем "KEY-XX.docx", где "KEY" - ключ таска (JRA-1, к примеру)
