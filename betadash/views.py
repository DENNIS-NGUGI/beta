from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'pages/index.html')

def agriculture(request):
    return render(request, 'pages/agriculture.html')

def about(request):
    return render(request, 'pages/about.html')

def msme(request):
    return render(request, 'pages/msme.html')

def pillars(request):
    return render(request, 'pages/pillars.html')

def projects(request):
    return render(request, 'pages/projects.html')

def uhc(request):
    return render(request, 'pages/uhc.html')

def housing(request):
    return render(request, 'pages/housing.html')

def digital(request):
    return render(request, 'pages/digital.html')

def login(request):
    return render(request, 'bauth/login.html')