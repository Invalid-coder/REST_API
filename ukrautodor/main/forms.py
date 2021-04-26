from django import forms

FUNC_CHOICES= [
    ('autocomplete', 'autocomplete'),
    ('BFS', 'BFS'),
    ('similar', 'similar'),
    ]

class UserForm(forms.Form):
     number = forms.CharField(max_length=100,  label='', widget=forms.TextInput(
                              attrs={'placeholder':'Искать здесь...', }))