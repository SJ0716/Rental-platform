

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_available = models.BooleanField(default=True)
    daily_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='일 단위 비용')  # 기본값 추가
    weekly_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='주 단위 비용')  # 기본값 추가
    def __str__(self):
        return self.title

class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', '대기 중'),
        ('Approved', '승인됨'),
        ('Rejected', '거절됨'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rental_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return f"{self.item.title} - {self.status}"

