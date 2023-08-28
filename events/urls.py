from django.urls import path
from . import views
app_name = 'events'
from events.admin import EventCategoryAdmin





urlpatterns = [
    path('categories/create/', views.EventCategoryCreateAPIView.as_view(), name='event_category_create'),
    path('', views.EventList.as_view(), name='event-list'),
    path('create/', views.EventCreate.as_view(), name='event-create'),
    path('<int:pk>/', views.EventUpdate.as_view(), name='event-update'),
    path('<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
    path('<int:event_id>/join/', views.join_event, name='join-event'),

    path('hashtags/', views.hashtags_list, name='hashtags-list'),
    path('hashtags/<int:pk>/', views.hashtags_detail, name='hashtags-detail'),

    path('filter/', views.filter_events, name='filter-events'),
    path('update_event_status/', views.update_event_status, name='update_event_status'),
    path('favourite_events/', views.FavouriteEventListCreateAPIView.as_view(), name='favourite-event-list-create'),
    path('follow/', views.FollowerListCreateAPIView.as_view(), name='follow-user'),
    path('reports/', views.ReportListCreateAPIView.as_view(), name='report-list-create'),
    path('reports/<int:pk>/', views.ReportRetrieveUpdateDestroyAPIView.as_view(), name='report-retrieve-update-destroy'),
    path('reactions/', views.ReactionListCreateAPIView.as_view(), name='reaction-list-create'),
    path('reactions/<int:pk>/', views.ReactionRetrieveUpdateDestroyAPIView.as_view(), name='reaction-retrieve-update-destroy'),
    path('event_reactions/', views.EventReactionListCreateAPIView.as_view(), name='event-reactions'),
    
]
