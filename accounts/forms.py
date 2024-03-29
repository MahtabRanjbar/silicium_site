from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].help_text = "Required Letters, digits and @/./+/-/_ only. "  # None
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user_time'].disabled = True
            self.fields['is_author'].disabled = True

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'special_user_time', 'is_author']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
        



