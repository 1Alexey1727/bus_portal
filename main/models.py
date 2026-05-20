from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.username
    
class Application(models.Model):
    COURSE_CHOICES = [
        ('bus', 'Автобус'),
        ('electrobus', 'Электробус'),
        ('tram', 'Трамвай'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('transfer', 'Перевод по номеру телефона'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('studying', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course_name = models.CharField(max_length=50, choices=COURSE_CHOICES)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.course_name}"