from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def filter(request):
    return render(request, 'filter.html', {})

def request(request):
    return render(request, 'request.html', {})

def register_mentor(request):
    return render(request, 'register_mentor.html', {})

def register_mentee(request):
    return render(request, 'register_mentee.html', {})
    
def login(request):
    return render(request, 'login.html', {})