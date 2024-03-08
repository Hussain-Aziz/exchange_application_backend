from rest_framework.serializers import ModelSerializer
from users.models import *
from student.models import *

'''SAMPLE
class UserSeralizer_Map_Marker(ModelSerializer):
    last_location = SerializerMethodField() # this is a custom field that we will define below
    class Meta:
        model = User # this is the model that we are serializing
        fields = [
            "id", # this exists in the User model
            "name", # this exists in the User model
            "last_location", # this is a custom field that we defined above
        ]
        
    # some custom function to get the custom field
    def get_last_location(self, obj):
        if last_location := obj.last_location:
            return MiniLocationSerializer(last_location).data
        else:
            return None
'''
class TestSeralizer(ModelSerializer):
    class Meta:
        model = Test
        fields = [
            "test",
        ]