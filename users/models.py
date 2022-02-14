from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


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
    agency = models.CharField(max_length=16, choices=AGENCY_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
