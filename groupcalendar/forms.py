from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

from groupcalendar.models import Event, Recurrence

class EventAddForm(forms.ModelForm):
    # use datetimepicker from bootstrap
    start = forms.DateTimeField(
            widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm',
                                           'pickSeconds': False}))
    end = forms.DateTimeField(
            widget=DateTimePicker(options={'format': 'YYYY-MM-DD HH:mm',
                                           'pickSeconds': False}))

    day = forms.DateTimeField(
            widget=DateTimePicker(options={'format': 'YYYY-MM-DD',
                                           'pickTime': False}),
            required=False)

    # form fields for recurrent events
    recurrence = forms.ChoiceField(required=False, choices=Recurrence.FREQUENCIES)
    recurrence.choices.insert(0, ('','---------'))
    count = forms.IntegerField(required=False)
    until = forms.DateTimeField(
            widget=DateTimePicker(options={'format': 'YYYY-MM-DD',
                                           'pickTime': False}),
            required=False)


    def __init__(self, *args, **kwargs):
        super(EventAddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = ('name', 'start', 'end', 'day', 'whole_day', 'calendar', 'description', 'place',  )
