from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def filter(request):
    return render(request, 'filter.html', {})

def request(request):
    return render(request, 'request.html', {})