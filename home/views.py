from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    # return render(request, template_name='<h1>Welcome to homepage</h1')
    return HttpResponse('<h1>Welcome</h1>')