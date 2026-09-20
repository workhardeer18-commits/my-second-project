from django.contrib.auth.models import AbstractUser
from django.db import models


# ۱. تعریف مدل کاربر سفارشی
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    # فیلدهای first_name و last_name قبلاً در AbstractUser هستند،
    # نیازی به تعریف مجدد نیست مگر اینکه بخواهید تنظیمات خاصی داشته باشند.

    REQUIRED_FIELDS = ['email']  # این خط برای رفع خطای شما الزامی است

    def __str__(self):
        return self.username


# ۲. مدل Ticket
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('sent', 'Sent'),
        ('closed', 'Closed'),
        ('answered', 'Answered'),
    ]
    subject = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.subject


# ۳. مدل Conversation
class Conversation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='conversations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
