from django import forms

class TaskSearchForm(forms.Form):
    task_title = forms.CharField(label="Название задачи", max_length=100)
