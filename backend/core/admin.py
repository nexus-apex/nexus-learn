from django.contrib import admin
from .models import Course, Lesson, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "category", "duration_hours", "status", "created_at"]
    list_filter = ["category", "status"]
    search_fields = ["title", "instructor"]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course_title", "lesson_type", "duration_mins", "position", "created_at"]
    list_filter = ["lesson_type"]
    search_fields = ["title", "course_title"]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student_name", "student_email", "course_title", "progress", "score", "created_at"]
    list_filter = ["status"]
    search_fields = ["student_name", "student_email", "course_title"]
