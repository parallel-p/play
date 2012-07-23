from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'auth/registration.html', {'form': form})
