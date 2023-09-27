from django import forms

from .models import User


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1930, 2018)),
        label='Birthday'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'birthday']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
