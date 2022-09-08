from django import forms

from accounts.models import CustomUser


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = "Required Letters, digits and @/./+/-/_ only. "  # None
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['special_user_time'].disabled = True
        self.fields['is_author'].disabled = True

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'special_user_time', 'is_author']



