from django.core.management.base import BaseCommand
from faker import Faker
from users.models import CustomUser
from course.models import Course
from lesson.models import Lesson
from payment.models import Payment
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate data for users, courses, lessons and payments'

    def handle(self, *args, **options):
        self.generate_users()

        self.generate_courses()

        self.generate_lessons()

        self.generate_payments()

    def generate_users(self):
        fake = Faker()

        for _ in range(2):
            email = fake.email()
            password = '123qwe456rty'
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone_number = fake.numerify(text='###########')
            country = fake.country()

            user = CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                country=country,
                email_verificated=True,
                is_superuser=False,
                is_staff=False,
                is_active=True
            )
            user.set_password(password)
            self.stdout.write(f'Создан пользователь {email}')
            user.save()

    def generate_courses(self):
        courses_data = [
            {
                "title": "Как ничего не понять и не подать вида: Базовый курс",
                "description": "Этот курс обучит вас основам. Узнайте, как сохранять спокойствие и уверенность, даже когда вы ничего не понимаете."
            },
            {
                "title": "Как ничего не понять и не подать вида: Продвинутый курс",
                "description": "Погрузитесь глубже в тему. Научитесь использовать сложные термины и аргументы, чтобы скрыть свою некомпетентность."
            },
            {
                "title": "Как ничего не понять и не подать вида: Профи",
                "description": "Этот курс отлично подойдет тем кто строит карьеру блестящего менеджера, управленца, чиновника. Научитесь уверенно вести диалоги на любые темы, сохраняя абсолютное неведение по существу."
            }
        ]
        all_users = CustomUser.objects.all()
        for course_data in courses_data:
            course = Course.objects.create(
                title=course_data["title"],
                description=course_data["description"],
                owner=random.choice(all_users)
            )
            self.stdout.write(f'Создан курс: {course.title}')

            course.save()
    def generate_lessons(self):
        lessons_data = {
            "Как ничего не понять и не подать вида: Базовый курс": [
                {"title": "Основы",
                 "description": "Этот урок научит вас основам. Вы изучите, как избегать ответственности и сохранять уверенность, когда вы не в курсе ситуации."},
                {"title": "Искусство сохранения спокойствия",
                 "description": "Здесь вы узнаете техники дыхания и самоконтроля, которые помогут сохранять спокойствие в любой непонятной ситуации."}
            ],
            "Как ничего не понять и не подать вида: Продвинутый курс": [
                {"title": "Продвинутые техники",
                 "description": "Углубленный курс, посвященный сложным методам скрытия некомпетентности. Вы научитесь использовать сложный жаргон и техники отвлечения внимания."},
                {"title": "Мастерство ухода от ответа",
                 "description": "Этот урок раскрывает секреты эффективного ухода от прямых ответов, используя риторические приемы и логические ловушки."}
            ],
            "Как ничего не понять и не подать вида: Профи": [
                {"title": "Искусство управления вопросами",
                 "description": "Вы изучите, как задавать вопросы, которые помогут отвлечь собеседника и перевести разговор в нужное русло."},
                {"title": "Как стать мастером риторики",
                 "description": "Вы научитесь говорить убедительно и красиво, при этом избегая конкретики по существу."},
                {"title": "Техники эффективного общения без знаний",
                 "description": "Узнайте, как использовать невербальные сигналы и мимику для поддержания уверенности."}
            ]
        }
        all_users = CustomUser.objects.all()
        for course_title, lesson_data in lessons_data.items():
            course = Course.objects.get(title=course_title)
            for lesson in lesson_data:
                Lesson.objects.create(
                    course=course,
                    title=lesson["title"],
                    description=lesson["description"],
                    video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    owner=random.choice(all_users)
                )
                self.stdout.write(f'Создан урок: {lesson["title"]} для курса {course.title}')

    def generate_payments(self):
        users = CustomUser.objects.filter(is_staff=False)
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        payment_methods = ['cash', 'transfer']
        start_date = datetime(2023, 8, 1)
        end_date = datetime.now()
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days

        for _ in range(20):
            user = random.choice(users)
            course = random.choice(courses) if random.choice([True, False]) else None
            lesson = random.choice(lessons) if random.choice([True, False]) else None
            amount = round(random.uniform(500.00, 1000.00), 2)
            payment_method = random.choice(payment_methods)
            random_number_of_days = random.randrange(days_between_dates)
            payment_date = start_date + timedelta(days=random_number_of_days)

            payment = Payment.objects.create(
                user=user,
                payment_date=payment_date,
                paid_course=course,
                paid_lesson=lesson,
                amount=amount,
                payment_method=payment_method
            )
            self.stdout.write(f'Создан платеж {payment.id} от {user}')

            payment.save()
