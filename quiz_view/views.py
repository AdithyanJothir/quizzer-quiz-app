
from django.shortcuts import render
from django.shortcuts import render,redirect
import string,random
from .models import Quiz,Card,Answerer
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse



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
            try:
                quiz = Quiz()
                quiz.name = name
                quiz.user = user
                url = gen_unique_url()
                quiz.unique_url = url
                quiz.save()
                messages.success(request,'Quiz created!')
                return redirect('home')
            except:
                messages.error(request,'Quiz Creation Failed!')
                return redirect('home')
        else:
            messages.error(request,'Invalid Input!')
            return redirect('login')
  


def create_card(request,url = "None"):
    if request.method == 'POST':
        question = request.POST.getlist('question')
        answer = request.POST.getlist('answer')
        select = request.POST.getlist('selected')
        
        try:
            url = request.session.get('url')
            quiz = Quiz.objects.get(unique_url = url)
            no_of_cards = Quiz.objects.filter(unique_url = url).values('no_of_cards')
            no_of_cards = no_of_cards[0]['no_of_cards']
            if(no_of_cards == None):
                card_count = 0
                for i in range(len(question)):
                    card = Card()
                    card.question = question[i]
                    card.answer = answer[i]
                    card.quiz = quiz
                    if select == 'False':
                        select = False
                    else:
                        select = True
                    card.select = select
                    card.save() 
                    card_count+=1
                Quiz.objects.filter(unique_url = url).update(no_of_cards = card_count)
                del request.session['url']
                messages.success(request,'Card created!')
                return redirect('home')
            else:
               return redirect('answerers_list')
        except:
            return HttpResponse('''<script>alert("Please Enable Cookies!");window.location="/"</script>''')
        
    else:
        user = request.user
        url = f"http://adityanjothir.pythonanywhere.com/quiz/{url}"
        quiz = Quiz.objects.get(unique_url = url)
        no_of_cards = Quiz.objects.filter(unique_url = url).values('no_of_cards')
        no_of_cards = no_of_cards[0]['no_of_cards']
        request.session['url'] = url
        if(no_of_cards == None):
            url_author = Quiz.objects.filter(unique_url = url, user_id = user.id)
            request.session['url'] = url
            if(url_author):
                return render(request,'quiz_view/cards.html')
            else:
                return HttpResponse('''<script>alert("No Questions Added Yet");window.location="/"</script>''')
        else:
            return redirect('answerer')
        

def answer_quiz(request):
    try:
        if request.method == 'POST':
            
                url = request.session.get('url')
                quiz = Quiz.objects.get(unique_url = url)
                fields = Card.objects.filter(quiz = quiz).values_list('question','answer')
                true_or_false = Card.objects.filter(quiz = quiz).values_list('select')
                correct_answers = 0
                curr = ""
                true_or_false_list = []
                post_values = []
                fields = dict(fields)


                for answer in true_or_false:
                    curr = str(list(answer)[0])
                    if(curr == 'True'):
                        true_or_false_list.append(True)
                    else:
                        true_or_false_list.append(False)

                
                

                for i in range(len(fields)):
                    if(request.POST[str(i)] == 'True'):
                        post_values.append(True)
                    else:
                        post_values.append(False)

                        
                for i in range(len(fields)):
                    if(post_values[i] == true_or_false_list[i]):
                        correct_answers += 1
                
                
                url = request.session.get('url')
                answerer_name = request.session.get('answerer_name')
                quiz = Quiz.objects.get(unique_url = url)
                try:
                    answerer_ob = Answerer()
                    answerer_ob.name = answerer_name
                    answerer_ob.quiz = quiz
                    answerer_ob.correct_answer = (correct_answers/len(fields))*100
                    answerer_ob.save()    
                except:
                    messages.error(request,'Answering Failed!')
                    return redirect(answerers_list)
                return redirect(answerers_list)
            
                
        else:
            url = request.session.get('url')
            quiz = Quiz.objects.get(unique_url = url)
            fields = Card.objects.filter(quiz = quiz).values_list('question','answer')
            fields = dict(fields)
            length = len(fields)
            return render(request,'quiz_view/quiz.html',{'fields':fields,'length':length})
    except:
        return HttpResponse('''<script>alert("Invalid Url");window.location="/answerer/"</script>''')
           

def answerers_list(request):
    try:
        url = request.session.get('url')
        quiz = Quiz.objects.get(unique_url = url)
        answeres = Answerer.objects.filter(quiz = quiz)
        return render(request,'quiz_view/final_list.html',{"answeres":answeres})
    except:
        return HttpResponse('''<script>alert("Invalid Url");window.location="/login/"</script>''')

def answerer(request):
    if request.method == 'POST':
        answerer_name = request.POST.get('name')
        request.session['answerer_name'] = answerer_name
        return redirect('answer_quiz')    
    else:
        return render(request,'quiz_view/answerer_name.html')
       
            


def gen_unique_url():
    count = 0
    s = 10
    url = ''
    while(True):  
        url = ''.join(random.choices(string.ascii_uppercase + string.digits, k = s))   
        ob = Quiz.objects.filter(unique_url = url)
        if(not ob):
            url = f"http://adityanjothir.pythonanywhere.com/quiz/{url}"
            return (url)
        elif count>10:
            s += 1
        count +=1



    


