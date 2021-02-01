from django.db import models
from django.urls import reverse


class Stig(models.Model):
    finding_id = models.CharField(max_length=12)

    class Meta:
        ordering = ['finding_id']

    def __str__(self):
        return "Finding ID: {}".format(self.finding_id)
