from django import forms
from django.core.exceptions import ValidationError
import re


def validate_username(name):
    regex_name = re.compile(r""" ([a-z\s]+) """, re.VERBOSE | re.IGNORECASE)

    res = regex_name.fullmatch(name)

    if not res:
        raise ValidationError(
            "Username should be a plain texts. Spaces are allowed.")


class registrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20,
                           validators=[validate_username])
    description = forms.CharField(label="Description", widget=forms.Textarea)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
