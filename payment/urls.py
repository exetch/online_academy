from django.urls import path
from .views import PaymentListView, create_checkout_session, retrieve_checkout_session, payment_success, payment_cancel

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('create-checkout-session/<int:course_id>/', create_checkout_session, name='create-checkout-session'),
    path('retrieve-checkout-session/<str:session_id>/', retrieve_checkout_session, name='retrieve-checkout-session'),
    path('success/', payment_success, name='payment-success'),
    path('cancel/', payment_cancel, name='payment-cancel')
]
