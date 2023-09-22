from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

CASH_LEFT_AT_BRANCHES = (
    ("HEAD OFFICE","HEAD OFFICE"),
    ("DVLA BRANCH","DVLA BRANCH"),
    ("KEJETIA BRANCH","KEJETIA BRANCH"),
    ("MELCOM SANTASI","MELCOM SANTASI"),
    ("MELCOM SUAME","MELCOM SUAME"),
    ("MELCOM TANOSO","MELCOM TANOSO"),
)

class CloseAccount(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    mtn = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    express = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    ecobank = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    gtbank = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    calbank = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    fidelity = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    debit = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    over = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    shortage = models.DecimalField(max_digits=19, decimal_places=2, default=0.0,blank=True)
    cash_left_at1 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at2 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at3 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at4 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at5 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at6 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at7 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at8 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at9 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    cash_left_at10 = models.CharField(max_length=100, choices=CASH_LEFT_AT_BRANCHES, default="Select cash left @",blank=True)
    user1 = models.CharField(max_length=20, default="",blank=True)
    user2 = models.CharField(max_length=20, default="",blank=True)
    user3 = models.CharField(max_length=20, default="",blank=True)
    user4 = models.CharField(max_length=20, default="",blank=True)
    user5 = models.CharField(max_length=20, default="",blank=True)
    user6 = models.CharField(max_length=20, default="",blank=True)
    user7 = models.CharField(max_length=20, default="",blank=True)
    user8 = models.CharField(max_length=20, default="",blank=True)
    user9 = models.CharField(max_length=20, default="",blank=True)
    user10 = models.CharField(max_length=20, default="",blank=True)
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0.0, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.total)
