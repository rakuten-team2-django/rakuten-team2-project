from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def home(request):
    return render(request, 'reasonable_recommendation_app/home.html', {})

def test_koya(request):
    return render(request, 'test_koya.html', {})
def test_yuto(request):
    return render(request, 'test_yuto.html', {})

def test_bibek(request):
    return render(request, 'test_bibek.html', {})

def test_akiba(request):
    return render(request, 'reasonable_recommendation_app/test_akiba.html', {})

