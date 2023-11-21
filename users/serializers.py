from rest_framework import serializers
from payment.serializers import PaymentSerializer
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True, source='payment_set')
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'avatar', 'phone_number', 'country', 'payment_history']

    def to_representation(self, instance):
        """
           Если пользователь, делающий запрос, не является владельцем объекта, из результата удаляются чувствительные поля.
           В данном случае, удаляются поля: 'password', 'last_name', и 'payment_history'.
           Если пользователь является владельцем объекта, объект возвращается без изменений.
           """
        ret = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.user != instance:
            sensitive_fields = ['password', 'last_name', 'payment_history']
            for field in sensitive_fields:
                ret.pop(field, None)
        return ret
