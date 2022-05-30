from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def home(request):
    return render(request,'quiz_view/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            try:
                messages.success(request,f'Account Created')
                return redirect("login")
            except Exception as e:
                print(e)
                messages.error(request,f'{e}')
                return redirect("register")
    else:
        return render(request, 'quiz_view/register.html')

def login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            ob=auth.authenticate(request,username=uname,password=pswd)
            print(ob)
            if ob is not None:
                auth.login(request,ob)
                return redirect('home')
            else:
                messages.error(request,"User not found")
                return redirect('login')
        except Exception as e:
            messages.error(request,e)
            return redirect('login')
    else:
        return render(request,'quiz_view/login.html')



