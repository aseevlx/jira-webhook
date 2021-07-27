# Jira Webhook

## English version

### Description

A small Python server that listens to your Jira Webhooks and outputs a .docx file from a given Jira-task.  
Uses Python 3.6, Flask, docxtpl, pipenv.

It was used to automatically generate a vacation request.  
Final document is generated from template_opl.docx and will be saved with name "KEY-XX.docx" where "KEY" - key from the task (JRA-1, for example)  

* You may need to change some custom field names in the `custom_fields` variable from `start.py`
* You can also fork and customize anything you want

### Running

* Install virtual environment:
```
pipenv install
```

* Run:
```
flask run
```


## Russian version (Описание на русском):

Небольшой сервер на Python, который слушает Jira Webhooks и генерирует .docx файл на основе данных из Jira-таски.  
Использует Python 3.6, Flask, docxtpl, pipenv.

Использовался для автоматической генерации заявлений на отпуск.  
Итоговый документ генерируется из template_opl.docx и сохраняется с именем "KEY-XX.docx", где "KEY" - ключ таски (JRA-1, к примеру).

* Вам может понадобиться изменить некоторые кастомные имена полей в переменной `custom_fields` из `start.py`
* Вы также можете сделать форк и кастомизировать все, что захотите.