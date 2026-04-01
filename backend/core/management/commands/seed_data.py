from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, Lesson, Enrollment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusLearn with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuslearn.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Course.objects.count() == 0:
            for i in range(10):
                Course.objects.create(
                    title=f"Sample Course {i+1}",
                    instructor=f"Sample {i+1}",
                    category=random.choice(["technology", "business", "design", "marketing", "hr"]),
                    duration_hours=random.randint(1, 100),
                    status=random.choice(["draft", "published", "archived"]),
                    enrollments=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Course records created'))

        if Lesson.objects.count() == 0:
            for i in range(10):
                Lesson.objects.create(
                    title=f"Sample Lesson {i+1}",
                    course_title=f"Sample Lesson {i+1}",
                    lesson_type=random.choice(["video", "text", "quiz", "assignment"]),
                    duration_mins=random.randint(1, 100),
                    position=random.randint(1, 100),
                    content=f"Sample content for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Lesson records created'))

        if Enrollment.objects.count() == 0:
            for i in range(10):
                Enrollment.objects.create(
                    student_name=f"Sample Enrollment {i+1}",
                    student_email=f"demo{i+1}@example.com",
                    course_title=f"Sample Enrollment {i+1}",
                    progress=random.randint(1, 100),
                    score=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["enrolled", "in_progress", "completed", "dropped"]),
                    enrolled_date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 Enrollment records created'))
