from rest_framework import viewsets

from payment.models import Payment
from .models import Course
from .permissions import ModeratorEditPermissions, UserPaidContentPermissions
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            paid_courses_ids = Payment.objects.filter(user=user, paid_course__isnull=False).values_list('paid_course',
                                                                                                        flat=True)
            return Course.objects.filter(id__in=paid_courses_ids)
    serializer_class = CourseSerializer
    permission_classes = [ModeratorEditPermissions, UserPaidContentPermissions]
