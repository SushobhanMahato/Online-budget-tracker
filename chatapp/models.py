from django.db import models
from datetime import date
from django.contrib.auth.models import User


class TotalBudget(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='total')
    total_amount = models.FloatField(blank=False, null=False)
    savings_goal = models.FloatField(blank=False, null=False)
    start_date = models.DateField(default=date.today, auto_now=False)

class DailyExpance(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='daily')
    amount = models.FloatField(blank=False, null=False)
    date = models.DateField(default=date.today, auto_now=False)