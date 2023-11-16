from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class CLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'course')
    list_filter = ('title',)
    search_fields = ('id', 'title', 'description')
