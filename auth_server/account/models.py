import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, login_id, password=None):
        if not login_id:
            raise ValueError('login_id is required')
        user = self.model(login_id=login_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login_id = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login_id

    def update_password(self, new_password):
        self.set_password(new_password)
        self.save(update_fields=["password"])

    def update_login_id(self, new_login_id):
        self.login_id = new_login_id
        self.save(update_fields=["login_id"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    class Meta:
        db_table = 'account'
