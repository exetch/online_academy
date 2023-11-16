from rest_framework import serializers
from lesson.models import Lesson
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()