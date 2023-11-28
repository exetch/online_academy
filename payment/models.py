from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('course.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey('lesson.Lesson', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=(('cash', 'Наличные'), ('transfer', 'Перевод на счет')), verbose_name='Способ оплаты')
    amount = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f"Платеж {self.id} от {self.user}"

class PaymentSession(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='оплата курса')
    session_id = models.CharField(max_length=255)
    url = models.URLField(max_length=400)
    status = models.CharField(max_length=100, default='created')


    def __str__(self):
        return f"{self.course.name} - {self.session_id}"