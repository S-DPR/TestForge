from django.db import models

class Account(models.Model):
    login_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
