from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello(request):
   text = """<h1>welcome to my app !</h1>"""
   # return HttpResponse(text)
   return render(request, 'index.html')

def test(request):
   text = """<h1>Test my app !</h1>"""
   return render(request, 'test.html')