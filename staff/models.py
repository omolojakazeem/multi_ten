from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from company.models import Company
from staff.customManager import CustomUserManager

now = str(timezone.now())
chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
UID_ENCODER = chars + now


def get_my_uiid(my_lenght, my_char):
    return get_random_string(my_lenght, my_char)


class UserType(models.Model):
    user_type = models.CharField(max_length=25, default='Admin')
    user_type_slug = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.user_type_slug = slugify(self.user_type)
        super(UserType, self).save(*args, **kwargs)

    def __str__(self):
        return self.user_type


class Staff(AbstractBaseUser, PermissionsMixin):
    uiid = models.CharField(max_length=500, editable=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    position = models.CharField(max_length=50, null=True, blank=True)
    manager = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    # staff_department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name='staff_dept')
    # staff_division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True, related_name='staff_division')
    employed_on = models.DateField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    personal_phone = models.CharField(max_length=35, blank=True, null=True)
    office_ext = models.IntegerField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        self.uiid = get_my_uiid(32, UID_ENCODER)
        super(Staff, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
