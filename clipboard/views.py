from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from .models import UserAccount, Word, User
from .forms import WordInputForm, UserAccountForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta,date

def view_deleted_words(request):
    if request.user.is_authenticated and request.method=='GET':

        words = Word.objects.filter(user=request.user,for_deletion=True).order_by('-date_added')
        context={'words':words,}
        return render(request,'clipboard/deleted_words.html',context)
    else:
        return redirect('loginPage')


def view_words(request,hours):
    if request.user.is_authenticated and request.method=='GET':
    
        
        if hours != 0:
            enddate = date.today() + timedelta(days=1)
            startdate = enddate - timedelta(days=(hours))
            
            words=Word.objects.filter(date_added__range=[startdate, enddate],user=request.user,for_deletion=False).order_by('-date_added')
            

        if hours == 0:
            words = Word.objects.filter(user=request.user,for_deletion=False).order_by('-date_added')
        context={'words':words,}
        return render(request,'clipboard/view_words.html',context)
    else:
        return redirect('loginPage')


def account_settings(request):
    if request.user.is_authenticated:
        userAccount=request.user.useraccount
        form=UserAccountForm(instance=userAccount)

        if request.method=="POST":
            form=UserAccountForm(request.POST, request.FILES ,instance=userAccount)
            if form.is_valid:
                form.save()
        context={'form':form}
        return render(request,'clipboard/account.html', context)

def hard_delete_words(request):
    if request.user.is_authenticated:
        print(request.POST.get('delete_all_confirm'))
        print(request.POST.get('delete_all'),"request.POST.get('delete_all'")
        if request.POST.get('delete_all') and request.POST.get('delete_all_confirm')=='delete' :
            words=Word.objects.filter(user=request.user.id,for_deletion=True)
            words.delete()

        return redirect('view_deleted_words')
    return redirect('login')

def delete_word(request,id):
    if request.user.is_authenticated:
        
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            if request.method=="POST":
                word_instance.delete()
                return redirect('add_word')
            context={'word_instance':word_instance}
            return render(request,'clipboard/delete_word.html',context)
        return redirect(request.path)
    return redirect('login')


def hide_word(request,id):
    if request.user.is_authenticated:
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            
            word_instance.for_deletion=True
            word_instance.save()
            return redirect('add_word')

        return redirect('add_word')
    return redirect('login')

def retrive_word(request,id):
    if request.user.is_authenticated:
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            word_instance.for_deletion=False
            word_instance.save()
            return redirect('add_word')
            
        return redirect('add_word')
    return redirect('login')


def view_word(request,id):
    if request.user.is_authenticated:
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            form=WordInputForm(instance=word_instance)

            context={'word_instance':word_instance ,'form':form}
            return render(request,'clipboard/view_word.html',context)
        return redirect('add_word')
    return redirect('login')

def edit_word(request,id):
    if request.user.is_authenticated:
        #word=Word.objects.get(id=id)
        #if word in request.user.word_set.all():
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            form=WordInputForm(instance=word_instance)

            if request.method=="POST":
                form=WordInputForm(request.POST,instance=word_instance)
                if form.is_valid():
                    new_word = form.save(commit=False)
                    new_word.user=request.user
                    new_word.save()
                    if 'redirect' in request.POST:
                        return redirect('add_word')
                    return redirect(request.path)
            context={'form':form}
            return render(request,'clipboard/edit_word.html',context)

    return redirect('add_word')




def add_word(request):
    if request.user.is_authenticated:
        if request.method=='POST':
           form=WordInputForm(request.POST)
           if form.is_valid():
               new_word = form.save(commit=False)
               new_word.user=request.user
               new_word.save() 
           return redirect('add_word')
        else:
            form=WordInputForm()
            #words=request.user.word_set.all()
            time_threshold = datetime.now() - timedelta(hours=240)
            words = Word.objects.filter(date_added__gte=time_threshold,user=request.user,for_deletion=False).order_by('-date_added')
            context={'words':words,'form':form}
            return render(request,'clipboard/add_word.html',context)
    else:
        return redirect('loginPage')

def register(request):
    if request.user.is_authenticated:
        return redirect('add_word')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            UserAccount.objects.create(user=user)
            return redirect('add_word')
    else:
        return render(request,'clipboard/register.html',context={'form':form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('add_word')
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('add_word')
        return redirect('loginPage')
    else:
        return render(request,'clipboard/login.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')