from django.core.management.base import BaseCommand
from Applogiq_assessment.models import PatientModel, ErrorChargeModel
from hl7apy.parser import parse_message
import os

class Command(BaseCommand):
    help = 'Parse HL7 files and store data in the database'

    def add_arguments(self, parser):
        parser.add_argument('./HL7', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['./HL7']
        with open(file_path, 'r') as file:
            hl7_data = file.read()

        hl7_message = parse_message(hl7_data)
        patient_info = self.extract_patient_info(hl7_message)
        errors = self.check_missing_fields(patient_info)
        self.store_patient_data(patient_info)
        self.store_error_charges(errors)
        self.stdout.write(self.style.SUCCESS('Successfully parsed and stored HL7 data'))

    def extract_patient_info(self, hl7_message):
        patient_info = {
            'first_name': hl7_message['PID']['PID.5']['PID.5.1'].value,
            'last_name': hl7_message['PID']['PID.5']['PID.5.2'].value,
            'date_of_birth': hl7_message['PID']['PID.7'].value,
            'mrn': hl7_message['PID']['PID.3']['PID.3.1'].value,
            'physician_name': hl7_message['ORC']['ORC.12'].value,
            'phone': hl7_message['PID']['PID.13'].value
        }
        return patient_info

    def check_missing_fields(self, patient_info):
        errors = []
        if not patient_info.get('date_of_birth'):
            errors.append('dob not found')
        if not patient_info.get('first_name') or not patient_info.get('last_name'):
            errors.append('patient name not found')
        if not patient_info.get('mrn'):
            errors.append('mrn not found')
        return errors

    def store_patient_data(self, patient_info):
        PatientModel.objects.create(
            first_name=patient_info['first_name'],
            last_name=patient_info['last_name'],
            date_of_birth=patient_info['date_of_birth'],
            mrn=patient_info['mrn'],
            physician_name=patient_info['physician_name'],
            phone=patient_info['phone']
        )

    def store_error_charges(self, errors):
        for error in errors:
            ErrorChargeModel.objects.update_or_create(
                error_type=error,
                defaults={'count': ErrorChargeModel.objects.filter(error_type=error).count() + 1}
            )
