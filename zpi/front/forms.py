from datetime import datetime

from django import forms


class ApplicationForm(forms.Form):
    name = forms.CharField(required=True, label='', widget=forms.TextInput(
        attrs={'autoComplete': "off"}))
    is_active = forms.BooleanField(required=False, initial=True)
    file = forms.FileField(required=True, label='')
    departments = forms.MultipleChoiceField(
        widget=forms.widgets.CheckboxSelectMultiple, required=True, label='')
    accepted_by = forms.ChoiceField(label='')

    def __init__(self, *args, **kwargs):
        accepted_by = (('s', 'Staff'), ('t', 'Teacher'), ('vd', 'Vice-dean'), ('d', 'Dean'),)
        choices = kwargs.pop('departments')
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['departments'].choices = [
            (choice['id'], choice['name']) for choice in choices]
        self.fields['accepted_by'].choices = accepted_by
        self.fields['accepted_by'].initial = 'd'

        if 'initial' not in kwargs:
            self.fields['departments'].initial = [choice['id']
                                                  for choice in choices]
        else:
            del self.fields['file']


class UserApplicationForm(forms.Form):
    CURRENT_DATE = forms.DateField(required=False, initial=datetime.today(
    ), widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'True'}))
    STUDENT_ID = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'autoComplete': "off", 'readonly': 'True'}))
    STUDENT_NAME_SURNAME = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'autoComplete': "off", 'readonly': 'True'}))
    STUDY_DEGREE = forms.ChoiceField(
        required=False, choices=((1, "I"), (2, "II")))
    STUDENT_SPECIALTY = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STUDENT_DIRECTION = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    STATIONARY = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'autoComplete': "off"}))
    OPINION = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": "4", 'autoComplete': "off"}))
    JUSTIFICATION = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"rows": "4", 'autoComplete': "off"}))
    WORK_SUPERVISOR = forms.CharField(required=False, )

    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data')
        user = kwargs.pop('user_data')
        super(UserApplicationForm, self).__init__(*args, **kwargs)
        self.fields['STUDENT_ID'].initial = user['email'].split('@')[0]
        self.fields['STUDENT_NAME_SURNAME'].initial = user['surname'] + ' ' + user['name']
        for field in list(self.fields):
            if field not in data:
                del self.fields[field]
            else:
                self.fields[field].required = data[field]


        # if 'initial' not in kwargs:
        #     self.fields['departments'].initial = [choice['id'] for choice in choices]
        # else:
        #     del self.fields['file']
