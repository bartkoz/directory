from rest_framework import serializers

from app.models import Teacher, Subject


class UploaderSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(self, obj):
        if obj.content_type not in ['application/zip', 'text/csv']:
            raise serializers.ValidationError('Only .zip and .csv files are allowed.')
        return obj


class CSVSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('name', )


class CSVLineSerializer(serializers.ModelSerializer):

    subjects_taught = CSVSubjectSerializer()
    profile_image = serializers.CharField()

    class Meta:
        fields = ('first_name', 'last_name', 'profile_picture', 'email_address', 'phone_number', 'room_number', 'subjects_taught')
        model = Teacher

    def validate_profile_image(self, value):
        if value:
            pass
