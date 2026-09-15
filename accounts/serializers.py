from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    date_joined = serializers.DateTimeField(read_only = True)

    class Meta:
        model = User 
        fields = ["name",'email','password','date_joined']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name",'email','date_joined']
        read_only_fields = ["id", "email", "date_joined"]
    
