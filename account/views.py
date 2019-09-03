from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from .forms import signupform, LoginForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
    else:
        form = signupform()
    return render(request, 'account/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            form.add_error(None, "아이디 또는 비밀번호가 올바르지 않습니다")

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('list')
