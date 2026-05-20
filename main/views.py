from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ApplicationForm, ReviewForm
from .models import Application, Review

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')

@login_required
def applications_view(request):
    user_applications = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'applications.html', {'applications': user_applications})

@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('applications')
    else:
        form = ApplicationForm()
    return render(request, 'create_application.html', {'form': form})

# Новый view для создания отзыва
@login_required
def create_review_view(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    
    # Проверка: можно оставить отзыв только если обучение завершено
    if application.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('applications')
    
    # Проверка: отзыв уже есть
    if hasattr(application, 'review'):
        messages.error(request, 'Вы уже оставили отзыв на эту заявку')
        return redirect('applications')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('applications')
    else:
        form = ReviewForm()
    
    return render(request, 'create_review.html', {'form': form, 'application': application})