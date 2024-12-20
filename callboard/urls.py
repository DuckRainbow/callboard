from django.urls import path, include
from rest_framework.routers import DefaultRouter

from callboard.apps import CallboardConfig
from callboard.views import (
    AdCreateAPIView,
    AdListAPIView,
    AdRetrieveAPIView,
    AdUpdateAPIView,
    AdDestroyAPIView,
    UsersAdListAPIView,

    FeedbackListAPIView,
    FeedbackCreateAPIView,
    UsersFeedbackListAPIView,
    FeedbackRetrieveAPIView,
    FeedbackUpdateAPIView,
    FeedbackDestroyAPIView,
)

app_name = CallboardConfig.name

router = DefaultRouter()

urlpatterns = [
                  path('', AdListAPIView.as_view(), name='ad_list'),
                  path('create/', AdCreateAPIView.as_view(), name='ad_create'),
                  path('my_ads/', UsersAdListAPIView.as_view(), name='ad_mylist'),
                  path('<int:pk>/', AdRetrieveAPIView.as_view(), name='ad_retrieve'),
                  path('<int:pk>/update/', AdUpdateAPIView.as_view(), name='ad_update'),
                  path('<int:pk>/delete/', AdDestroyAPIView.as_view(), name='ad_delete'),
                  path('<int:pk>/feedbacks/', FeedbackListAPIView.as_view(), name='feedback_list'),
                  path('<int:pk>/feedbacks/create/', FeedbackCreateAPIView.as_view(), name='feedback_create'),
                  path('my_list_feedbacks/', UsersFeedbackListAPIView.as_view(), name='feedback_mylist'),
                  path('feedbacks/<int:pk>/', FeedbackRetrieveAPIView.as_view(), name='feedback_retrieve'),
                  path('feedbacks/<int:pk>/update/', FeedbackUpdateAPIView.as_view(), name='feedback_update'),
                  path('feedbacks/<int:pk>/delete/', FeedbackDestroyAPIView.as_view(), name='feedback_delete'),
              ] + router.urls
