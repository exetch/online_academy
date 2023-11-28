import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from course.models import Course
from .models import Payment, PaymentSession
from .serializers import PaymentSerializer
from .services import create_stripe_product


stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date', 'amount']

class CreateCheckoutSessionView(APIView):

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            product, price = create_stripe_product(course)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price,
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            payment_session = PaymentSession(
                course=course,
                session_id=session.id,
                url=session.url,
                status='created'
            )
            payment_session.save()

            return Response(session)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveCheckoutSessionView(APIView):

    def get(self, request, session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return Response(session)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def payment_success(request):
    return HttpResponse("Оплата успешно завершена!")

def payment_cancel(request):
    return HttpResponse("Оплата отменена!")



