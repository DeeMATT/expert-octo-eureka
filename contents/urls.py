from django.urls import path

from .views import PageListView, PageDetailView


urlpatterns = [
    path('page/', PageListView.as_view()),
    path('page/<slug:slug>/', PageDetailView.as_view()),
]