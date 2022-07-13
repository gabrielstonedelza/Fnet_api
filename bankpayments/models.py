from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.utils.text import slugify
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


# Create your models here.

class PaymentAtBank(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    teller_name = models.CharField(max_length=100)
    teller_phone = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    d_200 = models.IntegerField(default=0, blank=True)
    d_100 = models.IntegerField(default=0, blank=True)
    d_50 = models.IntegerField(default=0, blank=True)
    d_20 = models.IntegerField(default=0, blank=True)
    d_10 = models.IntegerField(default=0, blank=True)
    d_5 = models.IntegerField(default=0, blank=True)
    d_2 = models.IntegerField(default=0, blank=True)
    d_1 = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        two_h_cedis_values = self.d_200 * 200
        one_h_cedis_values = self.d_100 * 100
        fifty_cedis_values = self.d_50 * 50
        twenty_cedis_values = self.d_20 * 20
        ten_cedis_values = self.d_10 * 10
        five_cedis_values = self.d_5 * 5
        two_cedis_values = self.d_2 * 2
        one_cedi_values = self.d_1 * 1

        self.total = Decimal(two_h_cedis_values) + Decimal(one_h_cedis_values) + Decimal(fifty_cedis_values) + Decimal(
            twenty_cedis_values) + Decimal(ten_cedis_values) + Decimal(five_cedis_values) + Decimal(
            two_cedis_values) + Decimal(one_cedi_values)
        print(self.total)
        print(self.amount)
        if not self.amount == self.total:
            raise ValueError("Your total is not equal to the amount")
        else:
            return
