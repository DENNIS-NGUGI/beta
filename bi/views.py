from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def bi_index(request):
    return render(request, 'pages/bi/index.html')

@login_required
def bi_agriculture(request):
    return render(request, 'pages/bi/agriculture.html')

@login_required
def bi_digital(request):
    return render(request, 'pages/bi/digital.html')

@login_required
def bi_housing(request):
    return render(request, 'pages/bi/housing.html')

@login_required
def bi_msme(request):
    return render(request, 'pages/bi/msme.html')

@login_required
def bi_uhc(request):
    return render(request, 'pages/bi/uhc.html')
