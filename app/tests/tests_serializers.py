from unittest import TestCase, mock

from django.core.files import File

from app.factories import TeacherFactory
from app.serializers import UploaderSerializer, CSVLineSerializer
from app.tests.tests_importer import map_csv_to_db


class SerializerTests(TestCase):
    def setUp(self):
        self.teacher = TeacherFactory

    def test_uploader_serializer(self):
        params = ["application/zip", "text/csv"]
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = "test"
        for content_type in params:
            with self.subTest():
                mock_file.content_type = content_type
                serializer = UploaderSerializer(data={"file": mock_file})
                self.assertTrue(serializer.is_valid())
        mock_file.content_type = "wrong"
        serializer = UploaderSerializer(data={"file": mock_file})
        self.assertFalse(serializer.is_valid())

    def test_csv_line_serializer(self):
        data = map_csv_to_db()
        data.pop("subjects_taught")
        serializer = CSVLineSerializer(data=data)
        self.assertTrue(serializer.is_valid())
