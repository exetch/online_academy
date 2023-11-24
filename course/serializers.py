from rest_framework import serializers
from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from .models import Course, Subscription


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count', 'lessons', 'owner', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(user=user, course=obj).first()
        return subscription.is_subscribed if subscription else False

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_lessons(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data