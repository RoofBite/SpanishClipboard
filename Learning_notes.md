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

# Debuging

## 1. login() takes 1 positional argument but 2 were given

view has the same name as the auth login function, so it is hiding it. Change the view name