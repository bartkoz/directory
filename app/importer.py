import copy
import csv
import io
import re
import unicodedata
from typing import Dict, Union
from zipfile import ZipFile, BadZipFile

from django.core.files.images import ImageFile

from app.models import Subject, Teacher


def map_csv_to_model_fields(row: Dict) -> Dict:
    row = {k.lower(): v for k, v in row.items()}
    csv_mapping = {'first name': 'first_name',
                   'last name': 'last_name',
                   'profile picture': 'profile_picture_name',
                   'email address': 'email_address',
                   'phone number': 'phone_number',
                   'room number': 'room_number'}
    data = dict()
    for csv_field, db_field in csv_mapping.items():
        data[db_field] = row.get(csv_field)
    return data


def import_csv(file: io.BytesIO) -> int:
    file = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))
    lines_imported = 0
    for line in reader:
        # parse data properly
        line = {k: unicodedata.normalize("NFKD", v).strip() for k, v in line.items()}
        # check if it consists of anything but spaces/empty strings
        if any(line):
            subjects_taught = line.pop('Subjects taught', None)
            mapped_row = map_csv_to_model_fields(line)
            if mapped_row.get('email_address'):
                teacher_obj, _ = Teacher.objects.update_or_create(email_address=mapped_row['email_address'],
                                                                  defaults=mapped_row)
                print(teacher_obj)
                current_subjects_teacher_count = teacher_obj.taught_subjects_count
                if subjects_taught:
                    for subject_name in re.split(', |,', subjects_taught):
                        subject, _ = Subject.objects.get_or_create(name=subject_name.lower())
                        if current_subjects_teacher_count >= 5:
                            teacher_obj.subjects_taught.add(subject)
                            current_subjects_teacher_count += 1
            lines_imported += 1
    return lines_imported


def import_zip(file: io.BytesIO) -> None:
    zfile = ZipFile(file, 'r')
    images = dict()
    for name in zfile.namelist():
        images[name] = ImageFile(io.BytesIO(zfile.read(name)), name=name)
    # Assign teachers their respective profile pictures
    for teacher in Teacher.objects.filter(profile_picture_name__isnull=True):
        try:
            teacher.profile_picture = images[teacher.profile_picture_name]
            teacher.save()
        except KeyError:
            continue


def perform_import(file: io.BytesIO) -> Union[int, None]:
    content_type = file.content_type
    if content_type == 'application/zip':
        return import_zip(copy.copy(file))
    elif content_type == 'text/csv':
        return import_csv(file)
