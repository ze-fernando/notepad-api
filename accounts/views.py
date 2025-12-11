from http import HTTPStatus
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.exceptions import ValidationError

from .serializers import LoginSerializer, RegisterSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {
                'message': 'Invalid Credentials',
                'token': None,
                'user': None,
            },
            status=HTTPStatus.UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
            {
                'message': 'Login Success',
                'token': token.key,
                'user': user.email,
            },
            status=HTTPStatus.OK
    )

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            'message': 'Login Success',
            'token': token.key,
            'user': user.email,
        },
        status=HTTPStatus.CREATED
    )

