
from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
    STATUS_CHOICES = (
        ('1', 'active'),
        ('2', 'inactive'),
    )
    event_category = models.CharField(max_length=255)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='2')

    def __str__(self):
        return self.event_category

class Event(models.Model):
    STATUS_CHOICES = (
        ('1', 'pending'),
        ('2', 'approved'),
        ('3', 'suspended'),
        ('4', 'completed'),
     
    )
    title = models.CharField(max_length=255)
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='1')
    event_attendees = models.IntegerField(default=0, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.title} ({self.event_start_datetime}), Attendees: {self.event_attendees}, Location: {self.location}, Category: {self.category}, Status: {self.get_status_display()}"
    


class EventAttendees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"    

class Hashtags(models.Model):
    STATUS_CHOICES = (
        ('1', 'pending'),
        ('2', 'approved'),
        ('3', 'suspended'),
       
     
    )
    hashtag_name = models.CharField(max_length=255)
  
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return self.hashtag_name
    

class Event_hashtags(models.Model):
    STATUS_CHOICES = (
        ('1', 'active'),
        ('2', 'inactive'),
    )
    hashtag = models.ForeignKey(Hashtags, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='2')

    def __str__(self):
        return f"{self.hashtag.hashtag_name} - {self.event.title}"    
    

class favouriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"    
    
class Follower(models.Model):
    STATUS_CHOICES = (
        ('1', 'active'),
        ('2', 'inactive'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='2')

    def __str__(self):
        return f"{self.user.username} is followed by {self.followed_by.username}"    
    

class Report(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Reported by: {self.reported_by.username}, Event: {self.event.title}"




class Reaction(models.Model):
    REACTION_CHOICES = (
        ('1', 'Like'),
        ('2', 'Love'),
        ('3', 'Wow'),
        ('4', 'Haha'),
        ('5', 'Sad'),
        ('6', 'Angry'),
    )
    STATUS_CHOICES = (
        ('1', 'active'),
        ('2', 'inactive'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='2')

    def __str__(self):
        return f"{self.user.username} - {self.reaction}"
    
class EventReaction(models.Model):
    STATUS_CHOICES = (
        ('1', 'active'),
        ('2', 'inactive'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='2')

    def __str__(self):
        return f"Event: {self.event.title}, User: {self.user.username}, Reaction: {self.reaction.reaction}"    
    



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.otp}'

