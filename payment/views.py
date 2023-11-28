import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
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

@csrf_exempt
def create_checkout_session(request, course_id):
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

    return JsonResponse({'sessionId': session.id, 'url': session.url})

def retrieve_checkout_session(request, session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        return JsonResponse(session)
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred'}, status=500)

def payment_success(request):
    return HttpResponse("Оплата успешно завершена!")

def payment_cancel(request):
    return HttpResponse("Оплата отменена!")



