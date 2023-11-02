from django.db import models
from django.conf import settings

class TennisCourt(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    court = models.ForeignKey(TennisCourt, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.court.name} booked by {self.user.username} on {self.start_time}'
