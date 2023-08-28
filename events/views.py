from httplib2 import Response
from rest_framework import generics, permissions
from .models import Event, EventCategory, EventAttendees, Hashtags, Event_hashtags, favouriteEvent, Follower,Report,Reaction,EventReaction
from .serializers import EventSerializer, EventCategorySerializer , EventAttendeesSerializer,FavouriteEventSerializer,FollowerSerializer,ReportSerializer, ReactionSerializer,EventReactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from geopy.distance import geodesic
from django.db.models import Q
from datetime import datetime, timedelta
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

#for creating event categories
class EventCategoryCreateAPIView(generics.CreateAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer

#for creating events and listing events

class EventList(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        my_lat = float(self.request.query_params.get('my_lat'))
        my_long = float(self.request.query_params.get('my_long'))
        radius = 10

        events = Event.objects.filter(status=2)

        filtered_events = []
        while not filtered_events and radius <= 100:
            for event in events:
                event_lat = event.latitude
                event_long = event.longitude
                distance = geodesic((my_lat, my_long), (event_lat, event_long)).km
              
                if distance <= radius:  
                    filtered_events.append(event)

            radius += 10

        return filtered_events

           
class EventCreate(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        event = serializer.save()  # Save the event instance
        hashtags = self.request.data.get('hashtag', [])  # Get the hashtags from the request data, default to an empty list

        with transaction.atomic():
            # Create the associations between the event and hashtags
            for hashtag_name in set(hashtags):
                try:
                    hashtag = Hashtags.objects.get(hashtag_name=hashtag_name)
                except Hashtags.DoesNotExist:
                    hashtag = Hashtags.objects.create(hashtag_name=hashtag_name, status='1')
                Event_hashtags.objects.create(event=event, hashtag=hashtag, status='1')




class EventUpdate(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@api_view(['POST'])
def join_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)

        # Check if the user has already joined the event
        if EventAttendees.objects.filter(user=request.user, event=event).exists():
            return Response({'error': 'You have already joined this event.'}, status=400)

        # Create an EventAttendees object for the user and event
        event_attendee = EventAttendees(user=request.user, event=event, status='joined')
        event_attendee.save()

        # Increment the event_attendees count by 1
        event.event_attendees += 1

        # Save the event model
        event.save()

        return Response({'message': 'Event joined successfully.'})
    except Event.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=404)

# hashtags event
@api_view(['GET', 'POST'])
def hashtags_list(request):
    if request.method == 'GET':
        hashtags = Hashtags.objects.all()
        data = [{'hashtag_name': hashtag.hashtag_name, 'status': hashtag.status} for hashtag in hashtags]
        return Response(data)
    elif request.method == 'POST':
        hashtag_name = request.data.get('hashtag_name')
        status = request.data.get('status')
        hashtag = Hashtags.objects.create(hashtag_name=hashtag_name, status=status)
        return Response({'message': 'Hashtag created successfully.'}, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def hashtags_detail(request, pk):
    try:
        hashtag = Hashtags.objects.get(pk=pk)
    except Hashtags.DoesNotExist:
        return Response({'error': 'Hashtag not found.'}, status=404)

    if request.method == 'GET':
        data = {'hashtag_name': hashtag.hashtag_name, 'status': hashtag.status}
        return Response(data)
    elif request.method == 'PUT':
        hashtag_name = request.data.get('hashtag_name')
        status = request.data.get('status')
        hashtag.hashtag_name = hashtag_name
        hashtag.status = status
        hashtag.save()
        return Response({'message': 'Hashtag updated successfully.'})
    elif request.method == 'DELETE':
        hashtag.delete()
        return Response({'message': 'Hashtag deleted successfully.'})




@api_view(['GET'])
def filter_events(request):
    title = request.GET.get('title', '')
    my_lat = float(request.GET.get('my_lat', 0))
    my_long = float(request.GET.get('my_long', 0))
    radius = float(request.GET.get('radius', 10))

    location = request.GET.get('location', '')
    start_datetime = request.GET.get('event_start_datetime', '')
    hashtag_id = request.GET.get('hashtag_id', '')

    events = Event.objects.all()

    if title:
        events = events.filter(title__icontains=title)

    if location:
        events = events.filter(location__icontains=location)

    if start_datetime:
        events = events.filter(event_start_datetime=start_datetime)

    if hashtag_id:
        events = events.filter(event_hashtags__hashtag_id=hashtag_id)

    filtered_events = []
    for event in events:
        event_lat = event.latitude
        event_long = event.longitude
        distance = geodesic((my_lat, my_long), (event_lat, event_long)).km
        if distance <= radius:
            filtered_events.append(event)

    serialized_data = EventSerializer(events.distinct(), many=True).data
    return Response(serialized_data)







def update_event_status(request):
    event_id = request.POST.get('event_id')
    new_status = request.POST.get('new_status')

    try:
        event = Event.objects.get(id=event_id)
        event.status = new_status
        event.save()

        response_data = {
            'success': True,
            'message': 'Event status updated successfully.',
            'new_status': event.get_status_display()  # Get the display value of the new status
        }
    except Event.DoesNotExist:
        response_data = {
            'success': False,
            'message': 'Event not found.'
        }

    return JsonResponse(response_data)


#fav events 
class FavouriteEventListCreateAPIView(generics.ListCreateAPIView):
    queryset = favouriteEvent.objects.all()
    serializer_class = FavouriteEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FollowerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#report
class ReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

class ReportRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


#for creating and getting reactions

class ReactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]        

    def perform_create(self, serializer):
        # Set the user as the authenticated user when creating a new reaction
        serializer.save(user=self.request.user)

class ReactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer    
    permission_classes = [permissions.IsAuthenticated]

# for giving reactions to a event
class EventReactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = EventReaction.objects.all()
    serializer_class = EventReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)