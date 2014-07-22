from django import forms
from rbmo.models  import WFPData, CoRequest

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
        'class' : 'form-control',
        'required' : 'True'
    }))

    jan = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    feb = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    mar = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    apr = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    may = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    jun = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    jul = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    aug = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    sept = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    oct = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    nov = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    dec = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))


    class Meta:
        model = WFPData
        fields = ['program','activity', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sept', 'oct', 'nov', 'dec']


class CORequestForm(forms.ModelForm):
    class Meta:
        model = CoRequest
        fields = ['subject', 'action', 'status']
        widgets = {
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
            })
        }
