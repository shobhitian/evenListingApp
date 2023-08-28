"""
URL configuration for eventListing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import RegisterAPI, LoginAPI, LogoutAPI, ActivateAccountView, ChangeStatusView,OTPRequestView,OTPVerificationView
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('events/', include('events.urls')),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('activate/', ActivateAccountView.as_view(), name='activate-account'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', LogoutAPI.as_view(), name='logout'),
    path('admin/events/eventcategory/<int:pk>/change_status/', ChangeStatusView.as_view(), name='change-status'),
    path('otp-request/', OTPRequestView.as_view(), name='otp-request'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp-verification'),
]



