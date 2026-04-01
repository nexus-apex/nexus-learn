import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Course, Lesson, Enrollment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['course_count'] = Course.objects.count()
    ctx['course_technology'] = Course.objects.filter(category='technology').count()
    ctx['course_business'] = Course.objects.filter(category='business').count()
    ctx['course_design'] = Course.objects.filter(category='design').count()
    ctx['course_total_rating'] = Course.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['lesson_count'] = Lesson.objects.count()
    ctx['lesson_video'] = Lesson.objects.filter(lesson_type='video').count()
    ctx['lesson_text'] = Lesson.objects.filter(lesson_type='text').count()
    ctx['lesson_quiz'] = Lesson.objects.filter(lesson_type='quiz').count()
    ctx['enrollment_count'] = Enrollment.objects.count()
    ctx['enrollment_enrolled'] = Enrollment.objects.filter(status='enrolled').count()
    ctx['enrollment_in_progress'] = Enrollment.objects.filter(status='in_progress').count()
    ctx['enrollment_completed'] = Enrollment.objects.filter(status='completed').count()
    ctx['enrollment_total_score'] = Enrollment.objects.aggregate(t=Sum('score'))['t'] or 0
    ctx['recent'] = Course.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def course_list(request):
    qs = Course.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(category=status_filter)
    return render(request, 'course_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def course_create(request):
    if request.method == 'POST':
        obj = Course()
        obj.title = request.POST.get('title', '')
        obj.instructor = request.POST.get('instructor', '')
        obj.category = request.POST.get('category', '')
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.status = request.POST.get('status', '')
        obj.enrollments = request.POST.get('enrollments') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/courses/')
    return render(request, 'course_form.html', {'editing': False})


@login_required
def course_edit(request, pk):
    obj = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.instructor = request.POST.get('instructor', '')
        obj.category = request.POST.get('category', '')
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.status = request.POST.get('status', '')
        obj.enrollments = request.POST.get('enrollments') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/courses/')
    return render(request, 'course_form.html', {'record': obj, 'editing': True})


@login_required
def course_delete(request, pk):
    obj = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/courses/')


@login_required
def lesson_list(request):
    qs = Lesson.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(lesson_type=status_filter)
    return render(request, 'lesson_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def lesson_create(request):
    if request.method == 'POST':
        obj = Lesson()
        obj.title = request.POST.get('title', '')
        obj.course_title = request.POST.get('course_title', '')
        obj.lesson_type = request.POST.get('lesson_type', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.position = request.POST.get('position') or 0
        obj.content = request.POST.get('content', '')
        obj.save()
        return redirect('/lessons/')
    return render(request, 'lesson_form.html', {'editing': False})


@login_required
def lesson_edit(request, pk):
    obj = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.course_title = request.POST.get('course_title', '')
        obj.lesson_type = request.POST.get('lesson_type', '')
        obj.duration_mins = request.POST.get('duration_mins') or 0
        obj.position = request.POST.get('position') or 0
        obj.content = request.POST.get('content', '')
        obj.save()
        return redirect('/lessons/')
    return render(request, 'lesson_form.html', {'record': obj, 'editing': True})


@login_required
def lesson_delete(request, pk):
    obj = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/lessons/')


@login_required
def enrollment_list(request):
    qs = Enrollment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(student_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'enrollment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def enrollment_create(request):
    if request.method == 'POST':
        obj = Enrollment()
        obj.student_name = request.POST.get('student_name', '')
        obj.student_email = request.POST.get('student_email', '')
        obj.course_title = request.POST.get('course_title', '')
        obj.progress = request.POST.get('progress') or 0
        obj.score = request.POST.get('score') or 0
        obj.status = request.POST.get('status', '')
        obj.enrolled_date = request.POST.get('enrolled_date') or None
        obj.save()
        return redirect('/enrollments/')
    return render(request, 'enrollment_form.html', {'editing': False})


@login_required
def enrollment_edit(request, pk):
    obj = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        obj.student_name = request.POST.get('student_name', '')
        obj.student_email = request.POST.get('student_email', '')
        obj.course_title = request.POST.get('course_title', '')
        obj.progress = request.POST.get('progress') or 0
        obj.score = request.POST.get('score') or 0
        obj.status = request.POST.get('status', '')
        obj.enrolled_date = request.POST.get('enrolled_date') or None
        obj.save()
        return redirect('/enrollments/')
    return render(request, 'enrollment_form.html', {'record': obj, 'editing': True})


@login_required
def enrollment_delete(request, pk):
    obj = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/enrollments/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['course_count'] = Course.objects.count()
    data['lesson_count'] = Lesson.objects.count()
    data['enrollment_count'] = Enrollment.objects.count()
    return JsonResponse(data)
