from django.urls import path
from .views import UserProfileListCreateView, UserProfileRetrieveUpdateDestroyView

urlpatterns = [
    path('api/profile/', UserProfileListCreateView.as_view(), name='create-profile'),
    path('api/profile/<int:pk>/', UserProfileRetrieveUpdateDestroyView.as_view(), name='retrieve-update-profile'),
]
