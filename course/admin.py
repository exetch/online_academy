from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description',)
    list_filter = ('title',)
    search_fields = ('id', 'title', 'description')

