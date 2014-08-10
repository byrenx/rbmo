from django import forms
from rbmo.models  import BudgetProposal, Agency
from django.contrib.auth.models import User

class BudgetProposalForm(forms.ModelForm):
    activity = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'required' : 'True'
    }))

    
    performance_indicator = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'required' : 'True'
    }))

    q1 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    q2 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    q3 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
    }))

    q4 = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'value' : '0'
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
        model = BudgetProposal
        fields = ['activity', 'allocation', 'performance_indicator', 'q1', 
                  'q2', 'q3', 'q4', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                  'jul', 'aug', 'sept', 'oct', 'nov', 'dec']
class LoginForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['email', 'acces_key']
        widgets = {'email': forms.TextInput(attrs={'class':'form-control', 'required': 'True', 'placeholder': 'Enter Email'}),
                   'acces_key': forms.PasswordInput(attrs={'class':'form-control','required': 'True', 'placeholder': 'Enter AccessKey'})}
