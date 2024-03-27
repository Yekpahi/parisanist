from django.db import models

class LaunchCountdown(models.Model):
    launch_date = models.DateTimeField()