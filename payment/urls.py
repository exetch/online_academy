from django.urls import path
from .views import PaymentListView, payment_success, payment_cancel, CreateCheckoutSessionView, \
    RetrieveCheckoutSessionView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('create-checkout-session/<int:course_id>/', CreateCheckoutSessionView.as_view(),
         name='create-checkout-session'),
    path('retrieve-checkout-session/<str:session_id>/', RetrieveCheckoutSessionView.as_view(),
         name='retrieve-checkout-session'),
    path('success/', payment_success, name='payment-success'),
    path('cancel/', payment_cancel, name='payment-cancel')
]
