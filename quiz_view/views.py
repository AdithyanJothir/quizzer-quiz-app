from enum import unique
from django.shortcuts import render
from django.shortcuts import render,redirect
import string,random
from quiz_view.models import Quiz,Card
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth



def home(request):
    if request.user.is_authenticated:
        quizes = Quiz.objects.filter(user = request.user)      
        return render(request,'quiz_view/home.html',{'quizes':quizes})
    else:
        return render(request,'quiz_view/login.html')

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

    else:
        return render(request, 'quiz_view/register.html')

def login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            ob=auth.authenticate(request,username=uname,password=pswd)
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

@login_required(login_url='/login/')
def create_quiz(request):
    if request.method == "POST":
        name = request.POST.get("quizname")
        user = request.user
        if(len(name)>0 and len(name)<=20):
            quiz = Quiz()
            quiz.name = name
            quiz.user = user
            url = gen_unique_url()
            quiz.unique_url = url
            quiz.save()
            messages.success(request,'Quiz created!')
            return redirect('home')
        else:
            messages.error(request,'Invalid Input!')
            return redirect('login')
  


def create_card(request,url = "None"):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        select = request.POST.get('selected')
        card = Card()
        url = request.session['url']
        quiz = Quiz.objects.get(unique_url = url)
        print(quiz)
        card.question = question
        card.answer = answer
        card.quiz = quiz
        if select == 'False':
            select = False
        else:
            select = True
        card.select = select 
        card.save() 
        messages.success(request,'card created!')
        return None
    else:
        user = request.user
        url = f"http://127.0.0.1:8000/quiz/{url}"
        url_author = Quiz.objects.filter(unique_url = url, user_id = user.id)
        if(url_author):
            request.session['url'] = url
            return render(request,'quiz_view/cards.html')
        else:
            return render(request,'quiz_view/home.html')


def gen_unique_url():
    count = 0
    s = 10
    url = ''
    while(True):  
        url = ''.join(random.choices(string.ascii_uppercase + string.digits, k = s))   
        ob = Quiz.objects.filter(unique_url = url)
        if(not ob):
            url = f"http://127.0.0.1:8000/quiz/{url}"
            return (url)
        elif count>10:
            s += 1
        count +=1



    


