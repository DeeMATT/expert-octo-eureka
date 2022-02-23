from rest_framework import serializers
from .models import Pages


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        # fields = "__all__"
        exclude = ['id']
        read_only_fields = ['published_at', 'updated_at']


def transformPage(data):
    title = data['title'].lower()

    return {
        title: data
    }

def transformPageDataSet(self):
    return list(map(lambda x: transformPage(x), self.data))
