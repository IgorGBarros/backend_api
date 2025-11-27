from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
)
from django.utils import timezone
from django.conf import settings


class Plan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_free = models.BooleanField(default=False)
    max_projects = models.IntegerField(default=1)
    max_users = models.IntegerField(default=1)
    max_storage_mb = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser deve ter is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def create_user_with_firebase(self, firebase_token, **extra_fields):
        try:
            from firebase_admin import auth as firebase_auth
            decoded_token = firebase_auth.verify_id_token(firebase_token)
            email = decoded_token.get('email')
            if not email:
                raise ValueError("Token do Firebase não contém email.")

            uid = decoded_token.get('uid')
            name = extra_fields.get('name') or uid

            user, created = self.get_or_create(
                email=email,
                defaults={'name': name, **extra_fields}
            )

            if created:
                user.set_unusable_password()
                user.save(using=self._db)

            return user

        except Exception as e:
            raise ValueError(f"Erro ao criar usuário com Firebase: {str(e)}")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    role = models.ForeignKey('User.Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    @property
    def is_pro_user(self):
        return self.plan and not self.plan.is_free


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    valid_until = models.DateTimeField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_active', 'valid_until']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name if self.plan else 'Sem plano'}"
    

class UserAnalytics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_logins = models.IntegerField(default=0)
    last_login_date = models.DateTimeField(null=True, blank=True)
    active_days_count = models.IntegerField(default=0)
    avg_session_duration_minutes = models.FloatField(default=0)
    features_used = models.JSONField(default=dict)  # ex: {"admin": 5, "api": 12}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics - {self.user.email}"