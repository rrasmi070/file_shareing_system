from django.contrib import admin
from django.urls import path, include

from api.views import FileUploadShare, Login, SharedFile, UserRegister

urlpatterns = [
    path('user_management/', UserRegister.as_view(), name='user_management'),
    path('login/', Login.as_view(), name='login'),
    path('file_upload_and_share/', FileUploadShare.as_view(), name='file_upload_and_share'),
    path('shared_file/', SharedFile.as_view(), name='shared_file'),
]
