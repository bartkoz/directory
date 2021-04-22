from django.urls import path

from app.views import UploaderAPIView, TeacherListAPIView, TeacherDetailAPIView

app_name = "directory"
urlpatterns = [
    path("directory/uploader/", UploaderAPIView.as_view()),
    path("directory/teachers/", TeacherListAPIView.as_view()),
    path("directory/teachers/<int:pk>/", TeacherDetailAPIView.as_view(), name="teacher_detail"),
]
