import re
from django.shortcuts import render
from django.http import HttpResponse



def Hello(request):
    context = {'name':"Macquena"}
    return render(request,'hello.html',context)
