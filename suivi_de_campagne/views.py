from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def context_processor(request):
    return ""
