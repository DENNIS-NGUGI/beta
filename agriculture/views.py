from django.shortcuts import render

def agriculture(request):
    return render(request, 'pages/agriculture/agriculture.html')
