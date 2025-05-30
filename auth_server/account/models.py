import uuid
from django.db import models

class Account(models.Model):
    class Meta:
        db_table = 'account'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
