from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

# Create your forms here.

class UserForm(UserCreationForm):
    '''
    This form is used to create a new usern using built in user form
    '''

    first_name = forms.CharField(max_length=100, required=True
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))  
    last_name = forms.CharField(max_length=100, required=True
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=100, required=True
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(max_length=100, required=True
        widget=forms.PasswordInput(attrs={'placeholder': 'Password 1','class':'password'}))
    password2 = forms.CharField(max_length=100, required=True
        widget=forms.PasswordInput(attrs={'placeholder': 'Password 2','class':'password'}))

    # captcha token

    token = forms.CharField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class AuthForm(AuthenticationForm):
    '''
    This form is used to authenticate a user
    '''
    username = forms.CharField(max_length=100, required=True
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, required=True
        widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'password'}))

    class Meta:
        model = User
        fields = ['username', 'password']




class UserProfileForm(ModelForm):
    '''
    This form is used to create a new user profile
    '''

    address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    town = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    county = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    post_code = forms.CharField(max_length=8, required=True, widget = forms.HiddenInput())
    country = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
    longitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())
    lattitude = forms.CharField(max_length=50, required=True, widget = forms.HiddenInput())


    class Meta:
        model = UserProfile
        fields = ['address', 'town', 'county', 'post_code', 'country', 'longitude', 'lattitude']