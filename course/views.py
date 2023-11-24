from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Course, Subscription
from .paginators import CoursePaginator
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
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied('User must be authenticated to create a course.')

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """
        При отправке POST-запроса на /subscriotions/{id}/subscribe/
        обновляет запись в Subscription, устанавливая is_subscribed = True
        """
        course = self.get_object()
        Subscription.objects.update_or_create(user=request.user, course=course, defaults={'is_subscribed': True})
        return Response({'status': 'subscribed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request, pk=None):
        """
        При отправке POST-запроса на /subscriptions/{id}/unsubscribe/
        обновляет запись в Subscription, устанавливая is_subscribed = False
        """
        course = self.get_object()
        subscription, created = Subscription.objects.get_or_create(user=request.user, course=course)
        subscription.is_subscribed = False
        subscription.save()
        return Response({'status': 'unsubscribed'}, status=status.HTTP_200_OK)