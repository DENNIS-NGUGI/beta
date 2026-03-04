from django.shortcuts import render

def dashboard(request):
    return render(request, 'pages/index.html')

def agriculture(request):
    return render(request, 'pages/agriculture.html')

def about(request):
    return render(request, 'pages/about.html')

def msme(request):
    return render(request, 'pages/msme.html')

def projects(request):
    return render(request, 'pages/projects.html')
