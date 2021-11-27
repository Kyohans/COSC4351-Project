from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from djchoices import ChoiceItem, DjangoChoices

from .managers import ReservationSystemUserManager

import random

class PaymentMethod(DjangoChoices):
    CASH = ChoiceItem('Cash')
    CREDIT = ChoiceItem('Credit')
    CHECK = ChoiceItem('Check')

class RegisteredUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    mailing_address = models.CharField(max_length = 60)
    billing_address = models.CharField(max_length = 60)
    diner_no = models.IntegerField(null = True)
    payment_method = models.CharField(max_length = 20, choices = PaymentMethod.choices)
    earned_points = models.IntegerField(default = 0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ReservationSystemUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.diner_no = random.randint(1,10)
        
        super().save(*args, **kwargs)

class RestaurantTable(models.Model):
    capacity = models.IntegerField()
    is_reserved = models.BooleanField(default = False)
    date_time = models.DateTimeField(null = True)
    user_first = models.CharField(max_length = 20, null = True)
    user_last = models.CharField(max_length = 20, null = True)
    user_phone = models.CharField(max_length = 20, null = True)
    user_email = models.CharField(max_length = 30, null = True)
    num_guests = models.IntegerField(null = True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if self.capacity not in (2, 4, 6, 8):
            raise ValidationError(
                _('Invalid field: %(value)s! Make sure table capacity is 2, 4, 6, or 8'),
                code = 'invalid',
                params = {'value': self.capacity}
            )
        
        super().save(*args, **kwargs)