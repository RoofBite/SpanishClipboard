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

# Debuging

## 1. login() takes 1 positional argument but 2 were given

view has the same name as the auth login function, so it is hiding it. Change the view name