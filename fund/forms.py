from django import forms
from rbmo.models  import AllotmentReleases
from django.contrib.auth.models import User
from wfp.forms import YearSelectForm

MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))

ALLOCATION = (('PS', 'Personal Services'),
              ('MOOE', 'Maintenance and Other Operating Expenses'),
              ('CO', 'Capital Outlay')
             )  



class MCASearchForm(YearSelectForm):    
    month = forms.ChoiceField(choices=MONTHS,
                              widget=forms.Select(attrs={
                                  'class': 'form-control'
                              }
    ))

    allocation  = forms.ChoiceField(choices=ALLOCATION,
                                    widget=forms.Select(attrs={
                                        'class': 'form-control'
                                    }
    ))



class AllotmentReleaseForm(forms.Form):
    MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))
    ada = forms.IntegerField(widget=forms.TextInput(attrs={
                            'class'    : 'form-control',
                            'required' : 'True'
    }))
    
    date_release = forms.DateField(widget=forms.DateInput(attrs={
        'class' : 'form-control',
        'type'  : 'date'
    }))

    allocation = forms.ChoiceField(choices=ALLOCATION,
                                   widget = forms.Select(attrs={
                                       'class' : 'form-control'
                                   })
    )

    month = forms.ChoiceField(choices=MONTHS,
                              widget=forms.Select(attrs={
                                  'class': 'form-control'
                              }
    ))
    amount = forms.DecimalField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'required': 'True'
        }
    ))


    class Meta:
        model = AllotmentReleases
        fields = ['ada', 'month', 'date_release', 'allocation','amount_release']



