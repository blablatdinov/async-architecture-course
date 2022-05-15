import datetime

from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import ManagementAward


class ManagementAwardView(APIView):

    def get(self, request):
        now_date = timezone.now()
        date = datetime.date(now_date.year, now_date.month, now_date.day)
        management_award = (
            ManagementAward.objects
            .filter(date=date)
            .first()
            .award
        )
        return Response(management_award, status=200)


urlpatterns = [
    path('api/v1/analytics/management-award/', ManagementAwardView.as_view())
]
