from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # date_joined = serializers.ReadOnlyField()
    # password = serializers.CharField(write_only=True)

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'date_joined': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                   last_name=validated_data['last_name'],
                                   first_name=validated_data['first_name']
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user
