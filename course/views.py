from rest_framework import viewsets

from .models import Course
from .permissions import ModeratorOrUser
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)
    serializer_class = CourseSerializer
    permission_classes = [ModeratorOrUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
