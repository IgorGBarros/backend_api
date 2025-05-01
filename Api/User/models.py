from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# Create your models here.
from firebase_admin import auth
import firebase_admin
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:  # Certifique-se de que a senha foi fornecida
            user.set_password(password)
        else:
            user.set_unusable_password()  # Define uma senha inutilizável
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    def create_user_with_firebase(self, firebase_token, **extra_fields):
        try:
            # Verifica o token do Firebase e obtém informações do usuário
            decoded_token = auth.verify_id_token(firebase_token)
            email = decoded_token.get('email')
            uid = decoded_token.get('uid')

            # Verifica se o usuário já existe no banco de dados
            user, created = self.get_or_create(email=email, defaults={'name': uid, **extra_fields})

            if created:
                user.set_unusable_password()  # Define uma senha inutilizável, pois o login é gerenciado pelo Firebase
                user.save(using=self._db)

            return user

        except Exception as e:
            raise ValueError("Erro ao verificar o token do Firebase ou ao criar usuário:", e)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    