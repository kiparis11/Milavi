from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from orders.models import Order

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('home')

    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
    }

    return render(request, 'users/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')


@login_required
def profile(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(
        request,
        'users/profile.html',
        {
            'orders': orders,
        }
    )