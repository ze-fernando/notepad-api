from rest_framework.serializers import CharField, EmailField, Serializer, ValidationError
from django.contrib.auth.models import User

class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True)


class RegisterSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True)
    email = EmailField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already extists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already extists")
        return value
