from rest_framework import serializers
from django.contrib.auth.hashers import make_password ,check_password

from api.models import SharedFiles, UserMaster
from api.token import generate_access_token, generate_refresh_token
from django.core.validators import FileExtensionValidator

from api.utills import EmallManagement


class UserListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = UserMaster
        # fields = '__all__'
        fields = ["profile","last_login","first_name","last_name","username","email","is_staff","is_active","is_deleted","created_by","created_on","updated_on","roles"]
    def get_profile(self, obj):
        request = self.context.get('request')
        # print(request)
        return f"{request.scheme}://" +f"{request.get_host()}/media/{obj.profile}" if obj.profile else ""
    
    
    
class LoginSerializer(serializers.Serializer):
    user_id = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)
    email = serializers.CharField(max_length=50, read_only=True)
    role = serializers.CharField(max_length=50, read_only=True)
    profile = serializers.CharField(max_length=50, read_only=True)
    
    access_token = serializers.CharField(max_length=50, read_only=True)
    refresh_token = serializers.CharField(max_length=50, read_only=True)
    
    class Meta:
        fields = ['user_id','password']
        
    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('user_id', None)
        password = attrs.get('password', None)
        user = UserMaster.objects.filter(username = username).last()
        print(make_password('Password@123'),"=====")
        if not user:
            raise serializers.ValidationError({'error':'Invalid User.'})
        if not check_password(password, user.password):
            raise serializers.ValidationError({'error':'Invalid Password.'})
        
        
        attrs['access_token'] = generate_access_token(user.id)
        attrs['refresh_token'] = generate_refresh_token(user.id)
        attrs['first_name'] = user.first_name
        attrs['last_name'] = user.last_name
        attrs['email'] = user.email
        attrs['role'] = user.roles
        attrs['profile'] = f"{request.scheme}://" +f"{request.get_host()}/media/{user.profile}" if user.profile else ""
        return attrs
    
class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    profile = serializers.ImageField()
    password = serializers.CharField(max_length=50)
    
    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')
        profile = attrs.get('profile')
        password = attrs.get('password')
        
        user_obj = UserMaster.objects.filter(email = email)
        if user_obj:
            raise serializers.ValidationError({'error': 'Email already exists.'})

        user = UserMaster()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = email
        user.profile = profile
        user.roles_id = 2
        user.password = make_password(password)
        user.save()
        
        
        reset_email = EmallManagement(
                to_list= [user_obj.last().email],
                cc_list= []
                
                
            )
        reset_email.register_user(password=password, username = email)
        
        return super().validate(attrs)
    
class FileUploadShareSerializer(serializers.Serializer):
    choice = UserMaster.objects.filter(roles_id=2).values_list('email', 'id')
    user = serializers.ChoiceField(choices = choice)
    files = serializers.FileField(validators=[FileExtensionValidator( ['CSV','PPTX','DOCX','XLXS'])])
    
class SharedFileSerializer(serializers.ModelSerializer):
    download_file = serializers.SerializerMethodField()
    class Meta:
        model = SharedFiles
        fields = '__all__'
        
    def get_download_file(self, obj):
        request = self.context.get('request')
        
        url = f"{request.scheme}://" +f"{request.get_host()}/download/{obj.token}" if obj.token else ""
        return url