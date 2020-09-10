from django import forms 
from .models import User,Profile
from django.contrib.auth.forms import UserCreationForm

## you cant directly use the UserCreation form
## because it wil ask for Username
## you have to set the your user model


class SignupForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ('email','password1','password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        ## exclude the user 
        ## it is filled bu signal dispacher
        exclude = ('user',)