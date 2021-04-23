from unittest import TestCase, mock
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.importer import map_csv_to_model_fields, perform_import


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
    def test_import_csv(self, mock_perform_import):
        mock_csv = mock.MagicMock(spec=InMemoryUploadedFile, name="test.csv")
        mock_csv.content_type = "text/csv"
        perform_import(mock_csv)
        mock_perform_import.assert_called_once_with(mock_csv)

    @mock.patch("app.importer.import_zip")
    def test_import_zip(self, mock_perform_import):
        mock_zip = mock.MagicMock(spec=InMemoryUploadedFile, name="test.csv")
        mock_zip.content_type = "application/zip"
        perform_import(mock_zip)
        mock_perform_import.assert_called_once_with(mock_zip)
