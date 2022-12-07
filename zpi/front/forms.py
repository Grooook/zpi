from django import forms


class ApplicationForm(forms.Form):
    name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'autoComplete': "off"}))
    is_active = forms.BooleanField(required=False)
    file = forms.FileField(required=True, label='')
    departments = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=True, label='')

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('departments')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['departments'].choices = [(choice['id'], choice['name']) for choice in choices]
        if 'initial' not in kwargs:
            self.fields['departments'].initial = [choice['id'] for choice in choices]
        else:
            del self.fields['file']
