from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        Widgets={
            'title':forms.TextInput(attrs = {
                'class':'form-control', 'placeholder':'Escribe el titulo de tu tarea'
            }),
            'description':forms.Textarea(attrs = {
                'class':'form-control', 'placeholder':'Escribe la descripcion de tu tarea'
            }),
            'important':forms.CheckboxInput(attrs = {
                'class':'form-check-input m-auto'               
            })
            
            
        }