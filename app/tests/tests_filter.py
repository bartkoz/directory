from unittest import TestCase

from app.factories import TeacherFactory
from app.filters import NameFilter
from app.models import Teacher


class FiltersTests(TestCase):
    def test_teacher_filter(self):
        teacher = TeacherFactory.create()
        checkup_letter = teacher.last_name[:1]
        filter = NameFilter(data={"teacher_filter": checkup_letter}, queryset=Teacher.objects.all())
        self.assertEqual(filter.qs.count(), 1)
