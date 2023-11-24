from django.conf import settings
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(upload_to='course_previews/', verbose_name='Превью', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} {'подписан' if self.is_subscribed else 'не подписан'} на {self.course.title}"