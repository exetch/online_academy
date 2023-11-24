import os
import sys
from datetime import datetime
import django
sys.path.append('C:/Users/ASUS/PycharmProjects/online_academy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.test import APITestCase
from users.models import CustomUser
from course.models import Course
from lesson.models import Lesson
from payment.models import Payment
from rest_framework import status

class CustomUserAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser@example.com', password='testpass123')
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(course=self.course, title="Test Lesson", description="Test Description",
                                       owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.user_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '123456789',
            'country': 'Test Country'
        }

    def test_create_user(self):
        response = self.client.post(f'/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_retrieve_user(self):
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)
        updated_data = {'first_name': 'Updated'}
        response = self.client.patch(f'/users/{self.user.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_delete_user(self):
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_read_other_user_data(self):
        other_user = CustomUser.objects.create(email='otheruser@example.com', password='otherpass123',
                                               last_name='OtherLastName', first_name='OtherFirstName',
                                               phone_number='89543211213')
        course = Course.objects.create(title="Test Course", description="Test Description", owner=other_user)
        lesson = Lesson.objects.create(course=course, title="Test Lesson", description="Test Description",
                                       owner=other_user)

        Payment.objects.create(
            user=other_user,
            payment_date=datetime.now(),
            paid_course=course,
            paid_lesson=lesson,
            amount=100.00,
            payment_method='transfer'
        )
        response = self.client.get(f'/users/{other_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)
        self.assertNotIn('last_name', response.data)
        self.assertNotIn('payment_history', response.data)

    def test_read_own_data(self):
        Payment.objects.create(
            user=self.user,
            payment_date=datetime.now(),
            paid_course=self.course,
            paid_lesson=self.lesson,
            amount=200.00,
            payment_method='cash'
        )
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('last_name', response.data)
        self.assertIn('payment_history', response.data)