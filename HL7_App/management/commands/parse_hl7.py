from datetime import datetime
import os
import hl7
from django.core.management.base import BaseCommand
from HL7_App.models import PatientModel, ErrorChargeModel

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        if not os.path.isdir(directory):
           return

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path) and file_path.endswith('.hl7'):
                try:
                    with open(file_path, 'r') as file:
                        hl7_data = file.read()

                    try:
                        hl7_message = hl7.parse(hl7_data)
                        if not hl7_message or not hl7_message[0]:
                            continue
                        
                        patient_info = self.extract_patient_info(hl7_message)
                        errors = self.check_missing_fields(patient_info)
                        self.store_patient_data(patient_info)
                        self.store_error_charges(errors)
                    except Exception as e:
                        print('Error', e)
                except Exception as e:
                    print('Error', e)
            else:
                print(f'Skipping: {file_path}')
        
        print('Successfully processed HL7 data from all files')

    def extract_patient_info(self, hl7_message):
        patient_info = {}
        try:
            pid_segment = hl7_message[0]
            
            patient_info = {
                'first_name': pid_segment[5][0] if len(pid_segment) > 5 and len(pid_segment[5]) > 0 else '',
                'last_name': pid_segment[5][1] if len(pid_segment) > 5 and len(pid_segment[5]) > 1 else '',
                'dob': self.parse_date(pid_segment[7]) if len(pid_segment) > 7 else '',
                'mrn': pid_segment[3][0] if len(pid_segment) > 3 and len(pid_segment[3]) > 0 else '',
                'physician_name': '',
                'phone': '', 
            }
        except IndexError as e:
           print(f'Error extracting patient information: {e}')
        return patient_info

    def parse_date(self, date_str):
        try:
            if isinstance(date_str, str):
                return datetime.strptime(date_str, '%Y%m%d').date()
        except ValueError:
            print(f'Invalid date format: {date_str}')
        return None

    def check_missing_fields(self, patient_info):
        errors = []
        if not patient_info.get('dob'):
            errors.append('dob not found')
        if not patient_info.get('first_name') or not patient_info.get('last_name'):
            errors.append('patient name not found')
        if not patient_info.get('mrn'):
            errors.append('mrn not found')
        return errors

    def store_patient_data(self, patient_info):
        if patient_info:
            PatientModel.objects.create(
                first_name=patient_info['first_name'],
                last_name=patient_info['last_name'],
                dob=patient_info['dob'],
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
