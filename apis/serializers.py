from rest_framework import serializers


class OrganizationNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, allow_blank=False, allow_null=False)
