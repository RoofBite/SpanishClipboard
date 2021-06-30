from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout

def add_word(request):
    return render(request,'clipboard/add_word.html')

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
    else:
        return render(request,'clipboard/login.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')