from django.urls import path
from .views import LessonListCreate, LessonRetrieveUpdateDestroy

urlpatterns = [
    path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroy.as_view(), name='lesson-detail'),
]