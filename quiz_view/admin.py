from django.contrib import admin
from quiz_view.models import Quiz,Card,Answerer
# Register your models here.

@admin.register(Quiz,Card,Answerer)
class AuthorAdmin(admin.ModelAdmin):
    pass
