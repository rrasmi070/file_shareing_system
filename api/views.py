import os
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from api.models import SharedFiles, UserMaster
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from api.permission import IsAdminUser, IsClientUser, IsDownloadUser
import uuid
from api.serializers import FileUploadShareSerializer, LoginSerializer, RegisterSerializer, SharedFileSerializer, UserListSerializer
from rest_framework.parsers import FormParser, MultiPartParser
import mimetypes
from file_shareing_system.settings import MEDIA_ROOT
from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view

# Create your views here.

class UserRegister(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (FormParser, MultiPartParser)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        if self.request.method == 'GET':
            return UserListSerializer
        
    def post(self, request, *args, **kwargs):
        serializer_class = RegisterSerializer(data = request.data)
        if serializer_class.is_valid():
            context = {'status':True, 'message': 'Successfully registered.', 'data': serializer_class.data}
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {'status':False, 'message': 'Successfully registered.', 'data': serializer_class.errors}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
            
            
    def get(self, request, *args, **kwargs):
        user_obj = UserMaster.objects.filter(roles = 2)
        serializer = UserListSerializer(user_obj, many = True, context = {'request': request})
        context = {'status':True, 'message': 'Success.', 'data':serializer.data}
        return Response(context, status=status.HTTP_201_CREATED)

class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LoginSerializer
    def post(self,request):
        # try:
            serializer = self.serializer_class(data=request.data, context = {'request': request})
            if serializer.is_valid():
                context = {'status': True, 'message': 'Sign In Successfully.', 'data': serializer.data}
                return Response(context, status = status.HTTP_200_OK)
            else:
                context = {'status': False, 'message': 'Invalid Credential.', 'data': serializer.errors}
                return Response(context, status = status.HTTP_200_OK)
            
        # except Exception as e:
        #     error = getattr(e, 'message', repr(e))
        #     logger.error(error)
        #     context = {'status': False,'message':'Something Went Wrong'}
        #     return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class FileUploadShare(generics.GenericAPIView):
    serializer_class = FileUploadShareSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated,IsAdminUser)
    
    def post(self, request, *args, **kwargs):
        
        serializer_class = FileUploadShareSerializer(data = request.data)
        if serializer_class.is_valid():
            obj = UserMaster.objects.filter(username=request.data.get('user')).last()
            files = request.data.getlist('files')
            if obj:
                for file in files:
                    file_obj = SharedFiles()
                    file_obj.token = uuid.uuid4()
                    file_obj.file = file
                    file_obj.shared_by_id = request.user.id
                    file_obj.shared_to_id = obj.id
                    file_obj.save()
            context = {'status': True, 'message': 'Sign In Successfully.', 'data': serializer_class.data}
            return Response(context, status = status.HTTP_200_OK)
        else:
            context = {'status': False, 'message': 'Invalid Credential.', 'data': serializer_class.errors}
            return Response(context, status = status.HTTP_200_OK)
        
class SharedFile(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsClientUser)
    serializer_class = SharedFileSerializer
    
    def list(self, request, *args, **kwargs):
        file_objs = SharedFiles.objects.filter(shared_to_id = request.user.id)
        serializer_class = self.serializer_class(file_objs, many = True, context = {'request': request})
        context = {'status': True, 'message': 'Sign In Successfully.', 'data': serializer_class.data}
        return Response(context, status = status.HTTP_200_OK)



class FileDownload(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,IsDownloadUser)
    def get(self, request, token):
        print (token)
        file_obj = SharedFiles.objects.filter(token = token).last()
        
        response = HttpResponse(file_obj.file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        return response