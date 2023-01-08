from rest_framework import serializers 
from .models import Tag,TaggedItem

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','label']
        


class TaggedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedItem
        fields = ['id','tag','content_type','object_id']
        