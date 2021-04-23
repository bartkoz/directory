from rest_framework import serializers
from django.urls import reverse

from app.models import Teacher


class UploaderSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(self, obj):
        if obj.content_type not in ["application/zip", "text/csv"]:
            raise serializers.ValidationError("Only .zip and .csv files are allowed.")
        return obj


class CSVLineSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "profile_picture_name",
            "email_address",
            "phone_number",
            "room_number",
            "subjects_taught",
        )
        model = Teacher


class TeacherDetailSerializer(serializers.ModelSerializer):
    subjects_taught = serializers.StringRelatedField(many=True)

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "profile_picture",
            "email_address",
            "phone_number",
            "room_number",
            "subjects_taught",
        )
        model = Teacher


class TeacherSerializer(TeacherDetailSerializer):

    teacher_details = serializers.SerializerMethodField()

    class Meta:
        fields = ("teacher_details", "first_name", "last_name", "subjects_taught")
        model = Teacher

    def get_teacher_details(self, obj):
        protocol = "https://" if self.context["request"].is_secure() else "http://"
        return (
            f'{protocol}{self.context["request"].get_host()}'
            f'{reverse("directory:teacher_detail", kwargs={"pk": obj.pk})}'
        )
