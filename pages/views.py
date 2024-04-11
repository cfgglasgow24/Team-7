from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def addEvent(request):
    return render(request, 'addEvent.html', {})

def cv(request):
    return render(request, 'cv.html', {})

def job_opportunities(request):
    return render(request, 'job_opportunities.html', {})

def login(request):
    return render(request, 'login.html', {})

def support (request):
    return render(request, 'support.html', {})

def mentorship (request):
    return render (mentorship, 'mentorship.html', {})