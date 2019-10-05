from django.shortcuts import render
import requests
import json

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')

def user(request):
    return render(request,'user.html')

def futureinvestments(request):
    return render(request,"futureinvestements.html")

def realestate(request):
    data = { 'city': 'mumbai', 'max_price': '50000' }
    r = requests.post("http://localhost:8080/api/get-housing/", data=data)
    import pdb; pdb.set_trace()
    res = r.json()
    return render(request, "realestate.html", {'response':r})