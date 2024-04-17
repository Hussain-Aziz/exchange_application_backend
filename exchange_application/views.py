from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework import permissions, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from users.models import Student, Faculty


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] # type: ignore
        login(request, user)

        if Student.objects.filter(user=user).exists():
            extra_data = {"is_faculty": False}
        elif Faculty.objects.filter(user=user).exists():
            extra_data = {"is_faculty": True,
                          "faculty_type": Faculty.objects.get(user=user).faculty_type}

        response = super(LoginView, self).post(request, format=None)
        response.data['user'].update(extra_data) # type: ignore
        return response