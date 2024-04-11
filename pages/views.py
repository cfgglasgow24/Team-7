from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def filter(request):
    return render(request, 'filter.html', {})

def request(request):
    return render(request, 'request.html', {})

def cv(request):
    return render(request, 'cv.html', {})

def filter(request):
    return render(request, 'filter.html', {})

def job_opportunities(request):
    return render(request, 'job_opportunities.html', {})

def login(request):
    return render(request, 'login.html', {})

def mentee_view(request):
    return render(request, 'mentee_view.html', {})

def mentor_view(request):
    return render(request, 'mentor_view.html', {})

def mentorship(request):
    return render(request, 'mentorship.html', {})

def register_mentee(request):
    return render(request, 'register_mentee.html', {})

def register_mentor(request):
    return render(request, 'register_mentor.html', {})

def support(request):
    return render(request, 'support.html', {})