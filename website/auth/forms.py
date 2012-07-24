from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name')
        model = User
