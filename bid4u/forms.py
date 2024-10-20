from django import forms
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

def validate_url_ends_with_digits(value):
    # Sprawdź, czy URL kończy się na cyfry
    if not re.search(r'\d+$', value):
        raise ValidationError('Sprawdź Twój link czy jest na pewno prawidłowy! Na końcu powinny być same cyfry.')


def validate_hexadecimal(value):
    if len(value) != 32:
        raise ValidationError('Pole musi mieć dokładnie 32 znaki.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Pole musi zawierać co najmniej jedną małą literę.')
    if not re.search(r'[0-9]', value):
        raise ValidationError('Pole musi zawierać co najmniej jedną cyfrę.')
    if not value.islower() or not value.isalnum():
        raise ValidationError('Pole może zawierać tylko małe litery i cyfry.')
    if value.isdigit():
        raise ValidationError('Pole nie może składać się wyłącznie z cyfr.')

def validate_alphanumeric(value):
    # Sprawdzenie, czy wartość jest alfanumeryczna, zawiera co najmniej jedną dużą literę, małą literę i cyfrę
    if not re.match(r'^[A-Za-z0-9]+$', value) or not re.search(r'[A-Z]', value) or not re.search(r'[a-z]', value) or not re.search(r'\d', value):
        raise ValidationError('CLIENT SECRET musi być alfanumeryczne i zawierać co najmniej jedną dużą literę, małą literę oraz cyfrę.')

class AccountForm(forms.Form):
    CLIENT_ID = forms.CharField(
        label='CLIENT ID',
        max_length=32,
        min_length=32,
        required=True,
        validators=[validate_hexadecimal],
        error_messages={
            'required': 'To pole jest wymagane.',
            'max_length': 'ID1 musi mieć dokładnie 32 znaki.',
            'min_length': 'ID1 musi mieć dokładnie 32 znaki.',

        }

    )
    CLIENT_SECRET = forms.CharField(
        label='CLIENT SECRET ',
        max_length=64,
        min_length=64,
        required=True,
        validators=[validate_alphanumeric]

    )

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'uk-input uk-margin-small'

class AuctionsForm(forms.Form):
    link = forms.URLField(label='Link do aukcji', max_length=200, validators=[validate_url_ends_with_digits])
    date_bid = forms.DateTimeField(label='Data złożenia oferty',
                                   widget=forms.DateInput(attrs={
        #'class':'form-control',
        #'type': 'date'
        'type': 'datetime-local',
        'step': '1'
        }
    ) , input_formats=['%Y-%m-%dT%H:%M:%S']

    )
    amount = forms.DecimalField(label='Kwota',
        max_digits=10,
        decimal_places=2,
        required=True)


    def __init__(self, *args, **kwargs):
        super(AuctionsForm, self).__init__(*args, **kwargs)
        now = timezone.localtime(timezone.now())
        self.fields['date_bid'].initial = now.strftime('%Y-%m-%dT%H:%M:%S')
        for visible_field in self.visible_fields():
            visible_field.field.widget.attrs['class'] = 'uk-input uk-margin-small'



