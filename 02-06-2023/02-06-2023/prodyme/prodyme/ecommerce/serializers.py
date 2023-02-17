from rest_framework import serializers

class categorySerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=100)

class subcategorySerializer(serializers.Serializer):
    item_category_name = serializers.CharField(max_length=100)

