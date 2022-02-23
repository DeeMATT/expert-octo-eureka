from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# from .views import PageListView, PageDetailView

# urlpatterns = [
#     path('pages/', PageListView.as_view()),
#     path('pages/<slug:slug>/', PageDetailView.as_view()),
# ]


router = DefaultRouter()
router.register(r'pages', views.PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]