from operator import mod
from django.db import models
from django.contrib.auth.models import User as U
from django.contrib.auth.models import AbstractUser
import string
import random

# Create your models here.

class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PayPlan(TimeStampedModel):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Organization(TimeStampedModel):
    class Industries(models.TextChoices):
        PERSONAL = 'persnal'
        RETAIL = 'retail'
        MANUFACTURING = 'manufacturing'
        IT = 'it'
        OTHERS = 'others'
    
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=15, choices=Industries.choices, default=Industries.OTHERS)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


#AUTH_USER_MODEL = "shortener.Users"
# 새로 Authuser를 상속받기 때문에 seetings에 위의 값을 따로 지정을 해줘야한다
class Users(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)


# class UserDetail(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE)
#     # user = models.OneToOneField(U, on_delete=models.CASCADE)
#     pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING)


class EmailVerification(TimeStampedModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Categories(TimeStampedModel):
    name = models.CharField(max_length=100)
    organiztion = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class ShortenedUrls(TimeStampedModel):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    prefix = models.CharField(max_length=50)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

