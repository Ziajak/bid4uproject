from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterFrom(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'password1': 'Hasło',
            'password2': 'Potwierdzenie hasła'
        }
        error_messages = {
            'password_mismatch': 'Podane hasła się nie zgadzają'
        }