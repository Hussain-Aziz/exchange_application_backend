from rest_framework import viewsets

from users.models import *
from student.models import *
from student.seralizers import *
from users.pagination import CustomPagination

'''SAMPLE
# get endpoint based on a model
class PocketLinks(viewsets.ReadOnlyModelViewSet):
    serializer_class = PocketLinkSerializer

    def get_queryset(self):
        if user_id:= self.request.query_params.get('user_id', None): # type: ignore
            return PocketLink.objects.filter(user__id=user_id)
        return PocketLink.objects.all()
    
    def search(self, devices):
        search_text = self.request.query_params.get('search_text', None) # type: ignore

        if search_text is None or search_text == '':
            return devices
        
        return devices.filter(
            Q(id__icontains=search_text) |
            Q(bLEname__icontains=search_text) |
            Q(nickname__icontains=search_text) |
            Q(serial__icontains=search_text)
        )
    
pocket_links = PocketLinks.as_view({'get': 'list'})

# arbitary endpoint
class SendPushNotification(APIView):
    """
    Sends a push notification to the provided users
    """
    def post(self, request):
        users = filter_users(request, User.objects.all())
        user_ids = users.values_list('id', flat=True)
        title = request.data.get('title', None)
        message = request.data.get('message', None)

        if user_ids is [] or title is None or message is None:
            return JsonResponse({'error': 'title, or message not provided'}, status=400)
        
        devices = FCMDevice.objects.filter(user__id__in=user_ids)
        print(title, message)
        try:
            send_fcm_message(devices, title, message)
        except Exception as e:
            return JsonResponse({'response': 'Error sending push notification to users', 
                                 'error': str(e),
                                 'users': list(user_ids)}, status=500)
        
        return Response({'response': "Sent push notification to the users ", 'users': list(user_ids)})
    
send_push_notification = SendPushNotification.as_view()

'''

class TestGet(viewsets.ModelViewSet):
    #serializer_class = TestSeralizer
    pagination_class = CustomPagination
    #permission_classes = [permissions.IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Test.objects.all()
    

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Student
from users.serializers import StudentApplicationSerializer

class StartApplicationAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StudentApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

