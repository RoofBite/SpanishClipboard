from django.shortcuts import render

def add_word(request):
    return render(request,'clipboard/add_word.html')
