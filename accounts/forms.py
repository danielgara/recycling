from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)   
        self.label_suffix = ''
        self.fields['email'].label = 'Email'
        self.fields['password2'].label = 'Confirm your password'
        for fieldname in ['username', 'password1', 'password2', 'email']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
