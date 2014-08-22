from django import forms
from rbmo.models  import *
from django.contrib.auth.models import User
from helpers.helpers import getYearsChoices

MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))


MONTHS2 = (('jan', 'January'), ('feb', 'February'), ('mar', 'March'), ('apr', 'April'), 
          ('may', 'May'), ('jun', 'June'), ('jul', 'July'), ('aug', 'August'), ('sept', 'September'),
          ('oct', 'October'), ('nov', 'November'), ('dec', 'December'))

RequirementsAllocation = (('PS', 'PS'), ('MOOE', 'MOOE'))

class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=100,
                               widget = forms.TextInput(attrs={
                                   'class' : 'form-control',
                                   'placeholder': 'Use your email as your Username',
                                   'required': 'True'
                               })
                           )

    first_name = forms.CharField(max_length=45,
                                 widget = forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Enter Firstname',
                                     'required' : 'True'
                                 })
    )

    last_name = forms.CharField(max_length=45,
                               widget = forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Enter Lastname',
                                   'required' : 'True'
                               })
    )

    group = forms.ModelChoiceField(queryset = Groups.objects.all(),
                               widget = forms.Select(attrs={
                                   'class': 'form-control'
                               })
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']



class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {'email': forms.TextInput(attrs={'class':'form-control', 'required': 'True', 'placeholder': 'Enter Email'}),
                   'password': forms.PasswordInput(attrs={'class':'form-control', 'required': 'True', 'placeholder': 'Password'})
        }
    

class AgencyForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'required': 'True',
        'placeholder' : 'Type the Name of Agency here..'
    }))

    email = forms.EmailField(max_length=75,
                             widget = forms.TextInput(attrs={
                                 'class' : 'form-control',
                                 'required': 'True',
                                 'placeholder': 'Type a valid email here..'
                             })
                         )
    
    sector = forms.ModelChoiceField(queryset = Sector.objects.all(),
                                   widget = forms.Select(attrs = {
                                       'class' : 'form-control'
                                   })
    )

    class Meta:
        model = Agency
        fields = ['name', 'email', 'sector']


class GroupForm(forms.Form):
    name = forms.CharField(max_length=75,
                           widget = forms.TextInput(attrs={
                               'class' : 'form-control',
                               'required': 'True'
                           })
    )

class MonthForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS,
                              widget = forms.Select(attrs={
                                  'class' : 'form-control'
                              })
    )


class ChangePassForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class' : 'form-control',
                 'required' : 'True'
             }
    ))

    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class' : 'form-control',
                 'required' : 'True'
             }
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class'    : 'form-control',
                 'required' : 'True'
             }
    ))
    


class AllocationMonthYearForm(forms.Form):
    allocation = forms.ChoiceField(choices=RequirementsAllocation,
                                   widget = forms.Select(attrs = {
                                       'class' : 'form-control'
                                   }))

    month = forms.ChoiceField(choices=MONTHS,
                              widget = forms.Select(attrs = {
                                  'class'  : 'form-control'
                              }))
    
    
    year = forms.ChoiceField(choices=getYearsChoices(),
                             widget = forms.Select(attrs = {
                                 'class' : 'form-control'
                             })
    )
