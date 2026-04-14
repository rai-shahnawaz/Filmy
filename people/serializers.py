from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.Serializer):
	uid = serializers.CharField()
	name = serializers.CharField()
	bio = serializers.CharField(allow_blank=True, required=False)
	birth_date = serializers.DateField(required=False, allow_null=True)
