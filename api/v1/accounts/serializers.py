from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='customuser-detail', read_only=True, lookup_field='id')
    
    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'avatar']
