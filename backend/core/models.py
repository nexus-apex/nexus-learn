from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255, blank=True, default="")
    category = models.CharField(max_length=50, choices=[("technology", "Technology"), ("business", "Business"), ("design", "Design"), ("marketing", "Marketing"), ("hr", "HR")], default="technology")
    duration_hours = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("draft", "Draft"), ("published", "Published"), ("archived", "Archived")], default="draft")
    enrollments = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255, blank=True, default="")
    lesson_type = models.CharField(max_length=50, choices=[("video", "Video"), ("text", "Text"), ("quiz", "Quiz"), ("assignment", "Assignment")], default="video")
    duration_mins = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student_name = models.CharField(max_length=255)
    student_email = models.EmailField(blank=True, default="")
    course_title = models.CharField(max_length=255, blank=True, default="")
    progress = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("enrolled", "Enrolled"), ("in_progress", "In Progress"), ("completed", "Completed"), ("dropped", "Dropped")], default="enrolled")
    enrolled_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.student_name
