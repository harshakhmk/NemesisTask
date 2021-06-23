from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ValidationError


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u"Email addresses must be unique.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserDetailsForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, required=False)
    username = forms.CharField(max_length=40, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("email", "username", "address")
