from django.contrib import admin
from .models import Game, Developer, Achievement, News

# Register your models here.

admin.site.register(Game)
admin.site.register(Developer)
admin.site.register(Achievement)
admin.site.register(News)

