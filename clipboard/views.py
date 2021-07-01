from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from .models import Word, User
from .forms import WordInputForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


def delete_word(request,id):
    if request.user.is_authenticated:
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
            if request.method=="POST":
                word_instance.delete()
                return redirect('add_word')
            context={'word_instance':word_instance}
            return render(request,'clipboard/delete_word.html',context)
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
                    return redirect('add_word')
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
            time_threshold = datetime.now() - timedelta(hours=24)
            words = Word.objects.filter(date_added__gt=time_threshold)
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
            form.save()
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