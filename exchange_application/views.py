from django.shortcuts import  get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import permissions, serializers, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
import uuid
from exchange_application.settings import EMAIL_HOST_USER
from student.utils import str2bool
from users.models import Student, Faculty, Admin, AccountActivation

def generate_activation_key():
    return str(uuid.uuid4())

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        u = User(username=validated_data['username'])
        u.set_password(validated_data['password'])
        u.save()
        activation_key = generate_activation_key()
        AccountActivation.objects.create(user=u, activation_key=activation_key)
        send_activation_email(u)
        return u

def send_activation_email(user: User):
    activation_key = AccountActivation.objects.get(user=user).activation_key
    activation_link = reverse('activate', kwargs={'activation_key': activation_key})
    activation_url = f"http://ausxchange.com/login{activation_link}"

    subject = "Activate Your AUS Exchange Portal Account"
    message = f"Dear user,\n\nPlease click the following link to activate your AUS Exchange Portal account:\n{activation_url}"
    send_mail(subject, message, EMAIL_HOST_USER, [user.username])

class ActivateAccountAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_key):
        activation_instance = get_object_or_404(AccountActivation, activation_key=activation_key)
        user = activation_instance.user
        user.is_active = True
        user.save()
        activation_instance.delete()  # Delete activation record after activation
        return Response({"message": "Your account has been activated successfully."})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class RegistrationAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        if str2bool(request.data['is_faculty']):
            Faculty.objects.create(user=user, faculty_type=request.data['faculty_type'], department=request.data['department'])
        else:
            Student.objects.create(user=user)
        
        user.is_active = False
        user.save()

        return Response({"user": UserSerializer(user).data, "message": "User created successfully."})

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] # type: ignore
        if not user.is_active:
            return Response({"error": "Your account is not activated yet."}, status=400)
        login(request, user)

        extra_data = {}
        if Student.objects.filter(user=user).exists():
            extra_data["is_faculty"] = False
        elif Faculty.objects.filter(user=user).exists():
            extra_data["is_faculty"] = True
            extra_data["faculty_type"] = Faculty.objects.get(user=user).faculty_type
        elif Admin.objects.filter(user=user).exists():
            extra_data["is_admin"] = True

        response = super(LoginView, self).post(request, format=None)
        if 'user' in response.data: # type: ignore
            user_data = response.data['user'] # type: ignore
            if isinstance(user_data, dict):  # Ensure it's a dictionary
                user_data.update(extra_data)

        return response

# class LoginView(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSerializer
#     throttle_classes = [AnonRateThrottle]

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user'] # type: ignore
#         login(request, user)

#         if Student.objects.filter(user=user).exists():
#             extra_data = {"is_faculty": False}
#         elif Faculty.objects.filter(user=user).exists():
#             extra_data = {"is_faculty": True,
#                           "faculty_type": Faculty.objects.get(user=user).faculty_type}
#         elif Admin.objects.filter(user=user).exists():
#             extra_data = {"is_admin": True}
        

#         response = super(LoginView, self).post(request, format=None)
#         response.data['user'].update(extra_data) # type: ignore
#         return response