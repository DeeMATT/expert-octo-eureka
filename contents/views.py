from .models import Pages
from .serializers import PageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys
class PageListView(APIView):
    """
    List all pages, or create a new page.
    """
    def get(self, request, format=None):
        pages = Pages.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        serializer = PageSerializer(data=data)
        if serializer.is_valid():

            body = data.get('body')
            # check if required fields are present in body object
            missingKeys = validateKeys(payload=body, requiredKeys=['html', 'css', 'js'])
            if missingKeys:
                raise serializers.ValidationError({
                    "body": "The body field should contain the key and values for: ['html', 'css', 'js']"
                })

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageDetailView(APIView):
    """
    Retrieve, update or delete a page instance.
    """
    def get_object(self, slug):
        try:
            return Pages.objects.get(slug=slug)
        except Pages.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        page = self.get_object(slug=slug)
        serializer = PageSerializer(page)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        page = self.get_object(slug)
        data = request.data
        serializer = PageSerializer(page, data=data)
        if serializer.is_valid():

            body = data.get('body')
            # check if required fields are present in body object
            missingKeys = validateKeys(payload=body, requiredKeys=['html', 'css', 'js'])
            if missingKeys:
                raise serializers.ValidationError({
                    "body": "The body field should contain the key and values for: ['html', 'css', 'js']"
                })
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        page = self.get_object(slug)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
