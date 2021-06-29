from django.shortcuts import render

def tmp_home(request):
    return render(request, 'index.html')