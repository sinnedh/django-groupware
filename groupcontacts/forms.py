from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from groupcontacts.models import Contact

class ContactAddForm(forms.ModelForm):
    birthdate = forms.DateTimeField(
            widget=DateTimePicker(options={'format': 'YYYY-MM-DD',
                                           'pickTime': False}),
            required=False)

    def __init__(self, *args, **kwargs):
        super(ContactAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
        fields = ['title', 'firstname', 'lastname', 'birthdate', 'note']
