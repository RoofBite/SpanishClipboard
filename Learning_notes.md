## Learned

## 1. Bootstrap button wihout shadow
``` html
<a href="#" class="btn shadow-none">View</a>
```

## 2. To get from users time form their time zones.
Set USE_TZ in setting to False
``` py
USE_TZ = False
```

## 3. Customize list of displayed fileds from model in admin panel
``` py

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display=('polish_word','spanish_word','etymology','date_added')

```

## 4. To display date and time without a.m and p.m in temalpate
``` html

{{word.date_added.date}}

{{ word.date_added|date:"H:i" }}
```

## 5. To format date and time in settings.py
``` py
USE_L10N = False

DATETIME_FORMAT = 'Y-m-d H:i'

DATE_FORMAT = 'Y-m-d'
```
## 6. To make ModelForm and connect instance to user
forms.py
``` py
class WordInputForm(forms.ModelForm):
    class Meta:
        model=Word
        exclude=('user',)
        fields=[
            'polish_word','spanish_word', 'etymology',
            'notes',
        ]
```
views.py
``` py
if request.method=='POST':
           form=WordInputForm(request.POST)
           if form.is_valid():
               new_word = form.save(commit=False)
               new_word.user=request.user
               new_word.save() 
```
I exclude user from form, next I check if form is valid, naxt I create new instance new_word but not saving it yet (new_word = form.save(commit=False)), at the end I set user filed of instance to request.user and instance is saved to datebase

## 7. Restrict user from seing edit page of item that is not conected to that user with ForeigKey
``` py

if request.user.is_authenticated:
        
        word_instance=Word.objects.filter(id=id,user=request.user.id).first()
        if word_instance:
```
OR
``` py
if request.user.is_authenticated:
        word=Word.objects.get(id=id)
        if word in request.user.word_set.all():
```
but secound solution is slower
## 8. To render form with filelds filed with data
``` py
form=WordInputForm(instance=word_instance)
```


# Debuging

## 1. login() takes 1 positional argument but 2 were given

View has the same name as the auth login function, so it is hiding it. Change the view name

## 2. The view clipboard.views.loginPage didn't return an HttpResponse object. It returned None instead.

I forgot to add redirect if user does not exist (for example wrong password was given), so I've changed this code:
``` py
if user is not None:
    login(request,user)
    return redirect('add_word')
        
```
to this:
```py
if user is not None:
    login(request,user)
    return redirect('add_word')
return redirect('loginPage')
```

