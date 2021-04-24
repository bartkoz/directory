from unittest.mock import ANY

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from app.factories import UserFactory, TeacherFactory, SubjectFactory


class APIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory
        self.teacher = TeacherFactory
        self.subject = SubjectFactory

    def test_uploader_get_no_login(self):
        r = self.client.get(reverse("directory:teacher_uploader"))
        self.assertEqual(r.status_code, 403)

    def test_uploader_post_no_login(self):
        r = self.client.post(reverse("directory:teacher_uploader"))
        self.assertEqual(r.status_code, 403)

    def test_uploader_get_logged_in(self):
        user = self.user.create()
        self.client.force_authenticate(user=user)
        r = self.client.get(reverse("directory:teacher_uploader"))
        self.assertEqual(r.status_code, 200)

    def test_uploader_post_logged_in(self):
        user = self.user.create()
        self.client.force_authenticate(user=user)
        r = self.client.post(reverse("directory:teacher_uploader"))
        self.assertEqual(r.status_code, 200)

    def test_teacher_list(self):
        teacher = self.teacher.create()
        subject = self.subject.create()
        teacher.subjects_taught.add(subject)
        r = self.client.get(reverse("directory:teacher_list"))
        data = [
            {
                "teacher_details": ANY,
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "subjects_taught": [subject.name],
            }
        ]
        self.assertEqual(r.json(), data)
        self.assertEqual(r.status_code, 200)

    def test_teacher_detail(self):
        teacher = self.teacher.create()
        subject = self.subject.create()
        teacher.subjects_taught.add(subject)
        r = self.client.get(reverse("directory:teacher_detail", kwargs={"pk": teacher.pk}))
        data = {
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "profile_picture": ANY,
            "email_address": teacher.email_address,
            "phone_number": teacher.phone_number,
            "room_number": teacher.room_number,
            "subjects_taught": [subject.name],
        }
        self.assertEqual(r.json(), data)
        self.assertEqual(r.status_code, 200)
