from rest_framework import serializers
from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data