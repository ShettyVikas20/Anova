from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.file_upload, name='upload_to_google_drive'),
]