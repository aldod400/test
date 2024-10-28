from rest_framework import serializers

from utils.general_response import error_response
from .models import Role, UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate



class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = UserProfile
        fields = "__all__"    

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
    required=True,
    allow_blank=False,
    error_messages={
        'required': 'Please provide your email address.',
        'invalid' : 'Enter a valid email address.',
    }
    )
    
    address = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'required': 'Please provide your address.'}
    )
    
    city = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'required': 'Please provide your city.'}
    )
    
    role = serializers.ChoiceField(choices=Role.choices, default=Role.USER)
    # photo = serializers.ImageField(required = True, error_messages = {'required': 'Please provide your Photo.'})
      
    class Meta:
        model = UserProfile
        fields = '__all__'
        
        extra_kwargs = {
            'first_name' : {
                'required'   : True,
                'allow_blank': False
                },
            
            'last_name' : {
                'required'   : True,
                'allow_blank': False
                },
            'password' : {
                'required'      : True,
                'write_only'    : True,
                'min_length'    : 8,
                'error_messages': {
                    'required' : 'Please provide your password.',
                    'min_length': 'Password must be at least 8 characters long.',
                }
                },
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = UserProfile.objects.get(email = email)
        except UserProfile.DoesNotExist:
            user = None
        
        if user is None:
             raise serializers.ValidationError({"email": "Invalid email."})
        else:
            user = authenticate(username = email, password = password)
            if user is None:
                raise serializers.ValidationError({"password": "Invalid password."})
        
        if not user.is_active:
            raise serializers.ValidationError({"email": "User account is disabled."})
        
        data['user'] = user
        return data
    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if not UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters or numbers.")
        return value

    def update_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        
        user = UserProfile.objects.get(email=email)
        user.password = make_password(password)
        user.save()
        return user