from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager as BaseUserManager
import string    
import random 


class UserManager(BaseUserManager):

    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    WFP = 1
    UN = 2

    PUBLIC_USER = 1
    CONTENT_EDITOR = 2
    ADMINISTRATOR = 3

    AGENCY_CHOICES = [
        (WFP, "wfp"),
        (UN, "un")
    ]

    ROLE_CHOICES = [
        (PUBLIC_USER, 'public_user'),
        (CONTENT_EDITOR, "content_editor"),
        (ADMINISTRATOR, "administrator")
    ]

    email_validator = EmailValidator()
    email = models.CharField(
        _('email address'),
        max_length=150,
        unique=True,
        validators=[email_validator],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    username = None
    agency = models.CharField(max_length=16, choices=AGENCY_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
