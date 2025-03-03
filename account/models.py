from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self,username, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not username:
            raise ValueError('The username is required')
        # email = self.normalize_email(email)
        # username =self.get_or_create(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,username, password=None, **extra_fields):
        
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email instead of username."""
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('email address', unique=True)
    
    # Add custom fields here
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username