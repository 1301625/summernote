from django.shortcuts import render,redirect

from django.contrib.auth import login

from .forms import signupform
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('')

    else:
        form = signupform()
    return render(request, 'account/signup.html',{'form':form})