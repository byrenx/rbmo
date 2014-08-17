from django import forms

MONTHS = ((1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
          (10, 'October'), (11, 'November'), (12, 'December'))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs = {
        'class' : 'form-control',
        'placeholder': 'Username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs = {
        'class' : 'form-control',
        'placeholder': 'Password'
    }))


class MonthForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS,
                              widget = forms.Select(attrs={
                                  'class' : 'form-control'
                              })
    )


