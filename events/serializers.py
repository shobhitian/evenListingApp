from rest_framework import serializers
from .models import  EventCategory, EventAttendees, Event, favouriteEvent, Follower, Report,Reaction,EventReaction
from django.db.models import Count

class EventSerializer(serializers.ModelSerializer):
    reaction_count = serializers.SerializerMethodField()

    def get_reaction_count(self, event):
        return EventReaction.objects.filter(event=event).count()

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'event_attendees': {'required': False}
        }


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'


class EventAttendeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAttendees
        fields = ['id', 'user', 'event', 'status']




class FavouriteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = favouriteEvent
        fields = ['id', 'user', 'event']        



class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

#create reaction
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'user', 'reaction', 'status')        
#giving reaction
class EventReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventReaction
        fields = '__all__'