from django.shortcuts import render

def msme(request):
    return render(request, 'pages/msme/msme.html')