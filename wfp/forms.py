from django import forms
from rbmo.models  import WFPData, CoRequest
from helpers.helpers import getYearsChoices


class YearSelectForm(forms.Form):
    year = forms.ChoiceField(choices = getYearsChoices(),
                                    widget = forms.Select(attrs = {
                                        'class' : 'form-control'
                                    }))



class WFPForm(forms.ModelForm):
    PROG = (('General Administration and Support Services', 'General Administration and Support Services'),
            ('Support to Operations', 'Support to Operations'),
            ('Operations', 'Operations'),
    )
    program = forms.ChoiceField(choices=PROG,
                                widget = forms.Select(attrs={
                                    'class': 'form-control'
                                })
    )
    activity = forms.CharField(widget=forms.TextInput(attrs={
        'required' : 'True',
        'class'    : 'form-control'
    }))

    jan = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    feb = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    mar = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    apr = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    may = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    jun = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    jul = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    aug = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    sept = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    oct = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    nov = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))

    dec = forms.DecimalField(widget=forms.NumberInput(attrs={
        'value' : '0'
    }))


    class Meta:
        model = WFPData
        fields = ['program','activity', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sept', 'oct', 'nov', 'dec']


class CORequestForm(forms.ModelForm):
    class Meta:
        model = CoRequest
        fields = ['date_received','subject', 'action', 'status', 'remarks']
        widgets = {
            'date_received': forms.DateInput(attrs={
                'type'     : 'date',
                'class'    : 'form-control',
                'required' : 'True',
                'style'    : 'width:200px'
            }),
            'subject' : forms.TextInput(attrs={
                'class'    : 'form-control',
                'required' : 'True'
            }),
            'action'  : forms.TextInput(attrs={
                'class'    : 'form-control',
                'required' : 'True'
            }),
            'status'  : forms.TextInput(attrs={
                'class'    : 'form-control',
                'required' : 'True'
            }),
            'remarks'  : forms.Textarea(attrs={
                'class'    : 'form-control',
                'required' : 'True',
                'rows'     : '5',
                'cols'     : '10'
            })
        }
