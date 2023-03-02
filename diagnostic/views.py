from copyreg import pickle
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from diagnosticService.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied
from .models import schueler, sitzungssummary, gast
from .serializers import schuelerSerializer, sitzungssummarySerializer
import random
from rest_framework import generics
from .sample_ratio_mismatch import sample_ratio_mismatch


class SchuelerViewSet(viewsets.ModelViewSet):
    """
    API endpoint to check user distribution among the intervention groups
    returns response SRM
    """

    queryset = schueler.objects.all()
    serializer_class = schuelerSerializer
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def check_user_distribution(self, request):
        try:
            auth = schueler.objects.get(Loginname=request.headers["Username"])
            response = sample_ratio_mismatch()
            return Response(response)
        except schueler.DoesNotExist:
            raise PermissionDenied()
