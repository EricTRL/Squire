from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import routers, viewsets
from rest_framework.views import APIView, Response

from .models import Committee
from .serializers import CommitteeSerializer 


def viewAllCommittees(request):
    serializer = CommitteeSerializer(Committee.objects.all(), many=True)
    return render(request, 'committees/view-all-committees.html', {"committees": serializer.data})
