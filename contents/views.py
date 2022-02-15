from .models import Pages
from .serializers import PageSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PageListView(APIView):
    """
    List all pages, or create a new page.
    """
    def get(self, request, format=None):
        snippets = Pages.objects.all()
        serializer = PageSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
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
        snippet = self.get_object(slug=slug)
        serializer = PageSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        page = self.get_object(slug)
        serializer = PageSerializer(page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        page = self.get_object(slug)
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
