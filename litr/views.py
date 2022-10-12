from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, 'litr/home.html')


@login_required
def posts(request):
    return render(request, 'litr/posts.html')


@login_required
def subscriptions(request):
    return render(request, 'litr/subscriptions.html')
