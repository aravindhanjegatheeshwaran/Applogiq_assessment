from django.db import models
from phone_field import PhoneField


class PatientModel(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    dob = models.DateField(null=True, blank=True)
    mrn = models.CharField(max_length=100)
    physician_name = models.CharField(max_length=25, blank=True)
    phone = PhoneField(blank=True)

    class Meta:
        db_table = 'Patient'


class EncounterChargesModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'EncounterCharges'


class ErrorChargeModel(models.Model):
    error_type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'ErrorCharge'