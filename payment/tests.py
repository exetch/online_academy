import os
import sys
from datetime import datetime, timedelta
import django
sys.path.append('C:/Users/ASUS/PycharmProjects/online_academy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.test import APITestCase
from users.models import CustomUser
from course.models import Course
from lesson.models import Lesson
from payment.models import Payment


class CustomUserAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser@example.com', password='testpass123')
        self.course1 = Course.objects.create(title="Test Course 1", description="Test Description 1", owner=self.user)
        self.course2 = Course.objects.create(title="Test Course 2", description="Test Description 2", owner=self.user)
        self.lesson1 = Lesson.objects.create(course=self.course1, title="Test Lesson 1", description="Test Description 1",
                                       owner=self.user)
        self.lesson2 = Lesson.objects.create(course=self.course2, title="Test Lesson 2",
                                             description="Test Description 2",
                                             owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_payment_filtering(self):
        payment1 = Payment.objects.create(user=self.user, payment_date=datetime.now(), paid_course=self.course1,
                                          paid_lesson=self.lesson1, amount=100.00, payment_method='cash')
        payment2 = Payment.objects.create(user=self.user, payment_date=datetime.now(), paid_course=self.course2,
                                          paid_lesson=self.lesson2, amount=200.00, payment_method='transfer')

        # Тест фильтрации по курсу
        response = self.client.get('/payments/', {'paid_course': self.course1.id})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], payment1.id)

        # Тест фильтрации по уроку
        response = self.client.get('/payments/', {'paid_lesson': self.lesson2.id})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], payment2.id)

        # Тест фильтрации по способу оплаты
        response = self.client.get('/payments/', {'payment_method': 'cash'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], payment1.id)

    def test_payment_ordering(self):
        payment1 = Payment.objects.create(user=self.user, payment_date=datetime.now() - timedelta(days=1),
                                          paid_course=self.course1, amount=100.00, payment_method='cash')
        payment2 = Payment.objects.create(user=self.user, payment_date=datetime.now(), paid_course=self.course2,
                                          amount=200.00, payment_method='transfer')

        # Тест сортировки по дате оплаты
        response = self.client.get('/payments/', {'ordering': 'payment_date'})
        self.assertEqual(response.data[0]['id'], payment1.id)
        self.assertEqual(response.data[1]['id'], payment2.id)

        # Тест сортировки по сумме оплаты
        response = self.client.get('/payments/', {'ordering': '-amount'})
        self.assertEqual(response.data[0]['id'], payment2.id)
        self.assertEqual(response.data[1]['id'], payment1.id)