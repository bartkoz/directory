from django.urls import path

from app.views import UploaderAPIEndpoint

app_name = 'directory'
urlpatterns = [
    path('directory/uploader/', UploaderAPIEndpoint.as_view())
]
