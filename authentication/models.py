from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password, **kwargs):
        # TODO improve it including in the client side.
        if not username or not email or not password:
            raise ValueError('The username, email, password are required.')

        account = self.model(
            email=self.normalize_email(email), username=username)
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, email, password, **kwargs):
        account = self.create_user(username, email, password, **kwargs)
        account.is_admin = True
        account.save()


@python_2_unicode_compatible
class Account(AbstractBaseUser):
    # Naive role implementation based on bit operations
    ROLE_USER = 0
    ROLE_ADMIN = 1
    ROLE_SUPERVISOR = 2
    ROLE_DEFAULT = ROLE_USER

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)

    # The is_admin flag is in the django sense, while the role is in our
    # business sense.
    is_admin = models.BooleanField(default=False)
    role = models.IntegerField(default=ROLE_DEFAULT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '%s (%s)' % (self.email, self.username)

    def get_short_name(self):
        return self.email
