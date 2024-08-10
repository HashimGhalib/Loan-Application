import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from enum import Enum
from datetime import date
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


# class LoanType(Enum):
#     PERSONAL = "Personal"
#     MORTGAGE = "Mortgage"


class LoanType(models.TextChoices):
    PERSONAL = 'PERSONAL', 'Personal Loan'
    MORTGAGE = 'MORTGAGE', 'Mortgage'



# Enum
    # status = models.CharField(
    #     max_length=20,
    #     choices=[(tag, tag.value) for tag in Status],
    #     default=Status.PENDING,
    # )


def path_and_rename(instance, filename):
    upload_to = 'profile_pictures/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Borrower(models.Model):
    borrower_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    profile_picture = models.ImageField(upload_to=path_and_rename,
                                        default='profile_pictures/default_profile_picture.png')
    email = models.EmailField(max_length=100, blank=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    phone_number = models.CharField(max_length=15)
    employment_history = models.CharField(max_length=300, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    # @property
    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Ensure no None values are returned unexpectedly
    #
    #     if self.income < 0:
    #         raise ValidationError(_("Income cannot be negative."))
    #
    #     return cleaned_data


class LoanApplication(models.Model):
    loan_application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    # loan_type = models.CharField(max_length=20, choices=[(tag, tag.value) for tag in LoanType], default=LoanType.PERSONAL)
    loan_type = models.CharField(
        max_length=10,
        choices=LoanType.choices,
        default=LoanType.PERSONAL
    )
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.05)
    loan_term = models.PositiveIntegerField()
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )


    # @property
    # def clean(self):
    #     if self.loan_term < 0:
    #         raise ValidationError(_("Loan term cannot be negative."))
    #     if self.loan_amount < 0:
    #         raise ValidationError(_("Loan amount cannot be negative."))
    #     if self.interest_rate < 0:
    #         raise ValidationError(_("Interest rate cannot be negative."))





# class Role(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#
#         return self.create_user(email, password, **extra_fields)
#
#     def get_by_natural_key(self, email):
#         # Use self.model here to reference the CustomUser model
#         return self.get(email=email)
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     # role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)
#     password = models.CharField(max_length=20, blank=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'password']
#
#     class Meta:
#         verbose_name = "Custom User"
#         verbose_name_plural = "Custom Users"
#
#     def __str__(self):
#         return f"{self.email} {self.first_name}"







# Create your models here.
