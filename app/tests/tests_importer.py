import io
from unittest import TestCase, mock

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.importer import map_csv_to_model_fields, perform_import, import_csv


def map_csv_to_db():
    line = {
        "First Name": "Laticia",
        "Last Name": "Landen",
        "Profile picture": "21167.JPG",
        "Email Address": "teacher1@school.com",
        "Phone Number": "+971-505-550-507",
        "Room Number": "3a",
        "Subjects taught": "Computer science, Physics",
    }
    return map_csv_to_model_fields(line)


class ImporterTests(TestCase):
    def test_map_csv_line(self):
        assert map_csv_to_db() == {
            "first_name": "Laticia",
            "last_name": "Landen",
            "profile_picture_name": "21167.JPG",
            "email_address": "teacher1@school.com",
            "phone_number": "+971-505-550-507",
            "room_number": "3a",
            "subjects_taught": "Computer science, Physics",
        }

    @mock.patch("app.importer.import_csv")
    def test_trigger_import_csv(self, mock_perform_import):
        mock_csv = mock.MagicMock(spec=InMemoryUploadedFile, name="test.csv")
        mock_csv.content_type = "text/csv"
        perform_import(mock_csv)
        mock_perform_import.assert_called_once_with(mock_csv)

    @mock.patch("app.importer.import_zip")
    def test_trigger_import_zip(self, mock_perform_import):
        mock_zip = mock.MagicMock(spec=InMemoryUploadedFile, name="test.csv")
        mock_zip.content_type = "application/zip"
        perform_import(mock_zip)
        mock_perform_import.assert_called_once_with(mock_zip)

    @mock.patch("csv.DictReader")
    @mock.patch("app.importer.map_csv_to_model_fields")
    @mock.patch("app.models.Subject.objects.get_or_create", return_value=(mock.MagicMock(), True))
    @mock.patch(
        "app.models.Teacher.objects.update_or_create",
        return_value=(mock.MagicMock(taught_subjects_count=0), True),
    )
    def test_perform_csv_import(
        self, teacher_create_mock, subject_create_mock, map_csv_mock, mock_csv_dictreader
    ):
        mock_csv_dictreader.return_value = [{"elem": "test"}]
        map_csv_mock.return_value = {
            "first_name": "Laticia",
            "last_name": "Landen",
            "profile_picture_name": "21167.JPG",
            "email_address": "teacher1@school.com",
            "phone_number": "+971-505-550-507",
            "room_number": "3a",
            "subjects_taught": "Computer science, Physics",
        }
        file_mock = mock.MagicMock(spec=File, wraps=io.BytesIO("test".encode("utf-8")))
        import_csv(file_mock)

        teacher_create_mock.assert_called_once()
        self.assertEqual(subject_create_mock.call_count, 2)
