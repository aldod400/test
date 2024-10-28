from django.shortcuts import render
from rest_framework.decorators import  api_view, permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import ForgetPasswordSerializer, LoginSerializer, RegisterSerializer, UserProfileSerializer
from utils.general_response import success_response, error_response

# Create your views here.

@api_view(['POST'])
def register(request):
    
    serializer = RegisterSerializer(data = request.data)

    if serializer.is_valid():
        if UserProfile.objects.filter(email = serializer.validated_data['email']).exists():
            return error_response(409, 'email already exist', 409)
       
        user_profile = UserProfile(
            first_name = serializer.validated_data['first_name'],
            last_name = serializer.validated_data['last_name'],
            email = serializer.validated_data['email'],
            password = make_password(serializer.validated_data['password']),
            address = serializer.validated_data['address'],
            city    = serializer.validated_data['city'],
            role  = serializer.validated_data['role'],
            photo = serializer.validated_data['photo'],
        )
        user_profile.save()
        token = Token.objects.create(user = user_profile)
        return success_response(201, 'your account registered successfully', {'User' : [{'id': user_profile.id}, serializer.data] , 'Token' : token.key})
    else:
        return error_response(400, serializer.errors, 400)

@api_view(['POST'])
def login(request):
    data = request.data
    # if 'email' not in data:
    #     return error_response(400, 'Email Field is requeired', 400)
    # if 'password' not in data:
    #     return error_response(400, 'Password Field is requeired', 400)

    # try:
    #     user = UserProfile.objects.get(email = data['email'])
    # except:
    #     user = None
    
    # if user is None:
    #     return error_response(404, 'invalid Email', 404)
    # else:
    #     user = authenticate(username = data['email'], password = data['password'])
    #     if user is None:
    #         return error_response(404, 'invalid Password', 404)
    serializer = LoginSerializer(data = data)
    if not serializer.is_valid():
        return error_response(400, serializer.errors, 400)
    user = serializer.validated_data['user']
    token, _  = Token.objects.get_or_create(user = user)
    serializer = UserProfileSerializer(user)
    return success_response(200, 'Login Successfully', {'User' : serializer.data, 'Token' : token.key})
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout(request):
    
        if request.user.auth_token.delete():
            return success_response(200, 'Successfully logged out.')
        
        return error_response(500, 'invalid Token', 500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserProfileSerializer(request.user)
    return success_response(200, 'Success', {'User' : serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_by_id(request, id):
    try:
        user = UserProfile.objects.get(id = id)
    except:
        user = None

    if user is None:
        return error_response(404, 'User Id Not found', 404)
    serializer = UserProfileSerializer(user)
    return success_response(200, 'Success', {'User' : serializer.data})

@api_view(['PUT'])
def forget_password(request):
    data = request.data
    # if 'email' not in data:
    #     return error_response(400, 'Please Inter the Email', 400)
    # if 'password' not in data:
    #     return error_response(400, 'Please Inter the Password', 400)
    # if 'password' in data and len(data['password']) < 8:
    #     return error_response(400, 'Passwod must be at least 8 Character or Numbers', 400)
        
    # try:
    #     user = UserProfile.objects.get(email = data['email'])
    # except:
    #     user = None
    
    # if user is None:
    #     return error_response(404, 'Email not Found', 404)
    
    # user.password = make_password(data['password'])
    # user.save()
    # serializer = UserProfileSerializer(user)
    serializer = ForgetPasswordSerializer(data = data)
    if not serializer.is_valid():
        return error_response(400, serializer.errors, 400)
    
    user = serializer.update_password()
    token, _  = Token.objects.get_or_create(user = user)
    user_data = UserProfileSerializer(user).data
    return  success_response(201, 'Password Created Successfully', {'User' :user_data, 'Token' : token.key})