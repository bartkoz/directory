from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.importer import perform_import
from app.serializers import UploaderSerializer


class UploaderAPIEndpoint(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploaderSerializer

    def get(self, request, *args, **kwargs):
        return Response({"Please upload csv or zip file."})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            lines_imported = perform_import(serializer.validated_data["file"])
            return Response(dict(success=True, lines_imported=lines_imported))
        return Response(dict(errors=serializer.errors))
