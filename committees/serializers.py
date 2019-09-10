from .models import Committee
from rest_framework import serializers


# The MemberSerializer converts the Member model to a Python dictionary
class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = "__all__"
        depth = 1
