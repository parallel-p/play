from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from system.views import index


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = UserCreationForm()
    return render(request, 'auth/registration.html', {'form': form})
