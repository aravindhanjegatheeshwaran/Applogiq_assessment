from django.db import models
from phone_field import PhoneField

class PatientModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    dob = models.DateField()
    mrn = models.IntegerField(unique=True)
    physician_name = models.CharField(max_length=25)
    phone = PhoneField(unique=True)


class EncounterChargesModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)


class ErrorChargeModel(models.Model):
    error_type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
