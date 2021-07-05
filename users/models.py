from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
import hashlib
import random
from django.core.mail import send_mail
from django.conf import settings


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    is_delete = models.BooleanField(default=False)

    age = models.PositiveIntegerField(verbose_name='Возраст', default=19)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(blank=True)
    activated = models.BooleanField('Активирован ли аккаунт', default=True)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        if not self.pk:

            self.activated = False
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]

            self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
            self.activation_key_expires = now() + timedelta(hours=48)

            send_mail(
                'Email from django',
                f"""
                Активируйте свой аккаунт
                http://127.0.0.1:8000/users/activate/{self.activation_key}/
                """,
                settings.EMAIL_HOST_USER,
                [self.email],
                # ['user3212name@gmail.com'],
                fail_silently=False
            )
        super().save(*args, **kwargs)
