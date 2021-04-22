import csv
import io
import re
import unicodedata
from typing import Dict
from zipfile import ZipFile

from django.core.files.images import ImageFile

from app.models import Subject, Teacher
from app.serializers import CSVLineSerializer


def map_csv_to_model_fields(row: Dict) -> Dict:
    row = {k.lower(): v for k, v in row.items()}
    csv_mapping = {
        "first name": "first_name",
        "last name": "last_name",
        "profile picture": "profile_picture_name",
        "email address": "email_address",
        "phone number": "phone_number",
        "room number": "room_number",
        "subjects taught": "subjects_taught",
    }
    data = dict()
    for csv_field, db_field in csv_mapping.items():
        data[db_field] = row.get(csv_field)
    return data


def import_csv(file: io.BytesIO) -> None:
    teacher_serializer = CSVLineSerializer
    file = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(file))
    for line in reader:
        # parse data properly
        line = {k: unicodedata.normalize("NFKD", v).strip() for k, v in line.items()}
        # check if it consists of anything but spaces/empty strings
        if any(line):
            mapped_row = map_csv_to_model_fields(line)
            subjects_taught = mapped_row.pop("subjects_taught", None)

            mapped_row = teacher_serializer(data=mapped_row)
            if mapped_row.is_valid():
                mapped_row = mapped_row.validated_data
                teacher_obj, _ = Teacher.objects.update_or_create(
                    email_address=mapped_row["email_address"], defaults=mapped_row
                )
                current_subjects_teacher_count = teacher_obj.taught_subjects_count
                if subjects_taught:
                    for subject_name in re.split(", |,", subjects_taught):
                        subject, _ = Subject.objects.get_or_create(name=subject_name.lower())
                        if current_subjects_teacher_count < 5:
                            teacher_obj.subjects_taught.add(subject)
                            current_subjects_teacher_count += 1


def import_zip(file: io.BytesIO) -> None:
    zfile = ZipFile(file, "r")
    images = dict()
    for name in zfile.namelist():
        name_lower = name.lower()
        images[name_lower] = ImageFile(io.BytesIO(zfile.read(name)), name=name_lower)
    # Assign teachers their respective profile pictures
    for teacher in Teacher.objects.filter(profile_picture_name__isnull=False):
        try:
            teacher.profile_picture = images[teacher.profile_picture_name.lower()]
            teacher.save()
        except KeyError:
            continue


def perform_import(file: io.BytesIO) -> None:
    content_type = file.content_type
    if content_type == "application/zip":
        return import_zip(file)
    elif content_type == "text/csv":
        return import_csv(file)
