from rest_framework import generics

from course.permissions import ModeratorEditPermissions
from .models import Lesson
from .serializers import LessonSerializer

class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ModeratorEditPermissions]

class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [ModeratorEditPermissions]
