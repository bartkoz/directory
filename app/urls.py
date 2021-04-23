from django.urls import path, re_path

from app.views import UploaderAPIView, TeacherListAPIView, TeacherDetailAPIView

app_name = "directory"
urlpatterns = [
    re_path(r"^directory/uploader/?$", UploaderAPIView.as_view(), name="teacher_uploader"),
    re_path(r"^directory/teachers/?$", TeacherListAPIView.as_view(), name="teacher_list"),
    path("directory/teachers/<int:pk>/", TeacherDetailAPIView.as_view(), name="teacher_detail"),
]
