from django.contrib.auth.models import Group
from django.conf import settings
from .models import Role, SharedFiles
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import permissions

# Admin Validation Permission Check.

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.roles.role,"======>>")
        try:
            roles = Role.objects.get(role='admin')
        except Role.DoesNotExist:
            roles = None
            pass
            # roles = Role.objects.create(role='Admin')
        if request.user.roles.role in ['admin'] :
            return request.user

# AreaManager User Validation Check.
class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.roles_id,"=====")
        try:
            roles = Role.objects.get(role='client')
        except Role.DoesNotExist:
            pass
        
        if request.user.roles_id in [1,2]:
            return request.user
        
        
class IsDownloadUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = view.__dict__['kwargs']['token']
            token_obj = SharedFiles.objects.filter(token = token).last()
            
        except Role.DoesNotExist:
            token = None
        if request.user.roles_id in [1,2]:
            try:
                if token_obj.shared_to.id in [request.user.id] or token_obj.shared_by.id in [request.user.id]:
                    return request.user
            except:
                return None