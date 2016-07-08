from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from chat.models import Account

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
