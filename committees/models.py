from django.db import models
from membership_file.models import Member
from achievements.models import Category


# Create categories for the Achievements like Boardgames, Roleplay, General
class Committee(models.Model):
    # basic info
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length = 63)
    description = models.TextField(max_length=255)

    members = models.ManyToManyField(Member, blank = True, related_name = "committee_members")


    def __str__(self):
        return self.name
