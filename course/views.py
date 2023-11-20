from rest_framework import viewsets
from .models import Course
from .permissions import ModeratorEditPermissions
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [ModeratorEditPermissions]
