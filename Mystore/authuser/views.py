from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
from .Serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view


class RegisterView(APIView):

    def post(self, request):
        data = {}
        username = request.data.get('username', False)
        email = request.data.get('email', False)
        city = request.data.get('city', False)
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        if not username:
            data["error"] = True
            data["message"] = "username is required"
        elif not email:
            data["error"] = True
            data["message"] = "email is required"
        elif not city:
            data["error"] = True
            data["message"] = "city is required"
        elif not phone:
            data["error"] = True
            data["message"] = "phone is required"
        elif not password:
            data["error"] = True
            data["message"] = "password is required"
        else:
            email_exists = User.objects.filter(email=self.request.data['email']).first()
            phone_exist = User.objects.filter(phone=self.request.data['phone']).first()
            if email_exists:
                data["error"] = True
                data["message"] = "email already exist"
            if phone_exist:
                data["error"] = True
                data["message"] = "phone already exist"
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save(
                password=make_password(self.request.data['password']))
            data['error'] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'registration success'
            data["created_at"] = account.created_at
            data['username'] = account.username
            data['email'] = account.email
            data['phone'] = account.phone
            data['city'] = account.city
            data['userid'] = f'{account.id}'
            token, create = Token.objects.get_or_create(user=account)
            data['token'] = token.key
        return Response(data)
    
    
@csrf_exempt
@api_view(['POST'])
def getToken(request):
    data = {}
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None and password is None:
        data["error"]=True
        data["message"] = "email or password blank"
    emailexist = User.objects.filter(email=email).exists()
    if not emailexist:
        data["error"]=True
        data["message"] = "wrong email"
    else:
        user = authenticate(email=email, password=password)
        if not user:
            data["error"]=True
            data["message"] = "wrong paswword"
        else:
            token, _ = Token.objects.get_or_create(user=user)

            account = user
            data["error"] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'login success'
            data['created_at'] = account.created_at
            data["username"] = account.username
            data["email"] = account.email
            data["phone"] = account.phone
            data["city"] = account.city
            data["userid"] = f'{token.user_id}'
            data["token"] = token.key
    return Response(data)




@api_view(['POST'])
def getSuperuser(request):
    data = {}
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None and password is None:
        data["error"] = True
        data["message"] = "email or password blank"
    emailexist = User.objects.filter(email=email).exists()
    if not emailexist:
        data["error"] = True
        data["message"] = "wrong email"
    else:
        user = authenticate(email=email, password=password)
        if not user:
            data["error"] = True
            data["message"] = "wrong paswword"
        elif not user.is_superuser:
            data["error"] = True
            data["message"] = "you are not a admin"
        else:
            token, _ = Token.objects.get_or_create(user=user)
            account = user
            data["error"] = False
            data["status_code"] = f'{status.HTTP_201_CREATED}'
            data['message'] = 'login success you are a admin'
            data['created_at'] = account.created_at
            data["username"] = account.username
            data["email"] = account.email
            data["phone"] = account.phone
            data["city"] = account.city
            data["userid"] = f'{token.user_id}'
            data["token"] = token.key
    return Response(data)

    
    

