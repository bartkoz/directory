from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.importer import perform_import
from app.models import Teacher
from app.serializers import UploaderSerializer, TeacherSerializer, TeacherDetailSerializer


class UploaderAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploaderSerializer

    def get(self, request, *args, **kwargs):
        return Response({"Please upload csv or zip file."})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            perform_import(serializer.validated_data["file"])
            return Response(dict(success=True))
        return Response(dict(errors=serializer.errors))


class TeacherListAPIView(ListAPIView):

    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeacherDetailAPIView(RetrieveAPIView):

    serializer_class = TeacherDetailSerializer
    queryset = Teacher.objects.all()
