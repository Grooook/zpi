from datetime import datetime

from django import forms


class ApplicationForm(forms.Form):
    name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'autoComplete': "off"}))
    is_active = forms.BooleanField(required=False)
    file = forms.FileField(required=True, label='')
    departments = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=True, label='')
    obligatory = forms.MultipleChoiceField(widget=forms.widgets.CheckboxSelectMultiple, required=True, label='')

    def __init__(self, *args, **kwargs):
        types = (('for_student', 'For student'), ('for_worker', 'For worker'))

        choices = kwargs.pop('departments')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['departments'].choices = [(choice['id'], choice['name']) for choice in choices]
        self.fields['obligatory'].choices = types
        self.fields['obligatory'].initial = ['for_student']

        if 'initial' not in kwargs:
            self.fields['departments'].initial = [choice['id'] for choice in choices]
        else:
            del self.fields['file']


class UserApplicationForm(forms.Form):
    CURRENT_DATE = forms.DateField(required=True, initial=datetime.today(), widget=forms.DateInput(attrs={'type': 'date'}))
    STUDENT_ID = forms.CharField(required=True, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STUDENT_NAME_SURNAME = forms.CharField(required=True, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STUDY_DEGREE = forms.ChoiceField(required=True, choices=((1,"I"),(2,"II")))
    STUDENT_SPECIALTY = forms.CharField(required=True, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STUDENT_DIRECTION = forms.CharField(required=True, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STATIONARY = forms.CharField(required=True, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    OPINION = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":"4", 'autoComplete': "off"}))
    JUSTIFICATION = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows":"4", 'autoComplete': "off"}))
    WORK_SUPERVISOR = forms.CharField(required=True, )

    def __init__(self, *args, **kwargs):
        super(UserApplicationForm, self).__init__(*args, **kwargs)
        # self.fields['departments'].choices = [(choice['id'], choice['name']) for choice in choices]
        # if 'initial' not in kwargs:
        #     self.fields['departments'].initial = [choice['id'] for choice in choices]
        # else:
        #     del self.fields['file']
