from rest_framework import serializers
from .models import Agency


class AgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Agency
        fields = ('id', 'name', 'sector', 'email', 'a_type')

    def create(self, validated_data):
        return Agency.objects.create(**validated_data)
        

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
