from rest_framework import serializers
from payment.serializers import PaymentSerializer
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True, source='payment_set')
    class Meta:
        model = CustomUser
        fields = "__all__"
