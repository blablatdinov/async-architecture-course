import datetime

from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import ManagementAward, CountPopugWithNegativeAward, MostExpensiveTask


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


class PopugWithNegativeAwardCount(APIView):

    def get(self, request):
        now_date = timezone.now()
        date = datetime.date(now_date.year, now_date.month, now_date.day)
        count_popug_with_negative_award = (
            CountPopugWithNegativeAward.objects
            .filter(date=date)
            .first()
            .award
        )
        return Response(count_popug_with_negative_award, status=200)


class MostExpensiveTaskView(APIView):

    def get(self, request):
        result = {}
        most_expensive_task_statistic = MostExpensiveTask.objects.values()
        for x in most_expensive_task_statistic:
            result[x['time_range']] = x['award']
        return Response(result)


urlpatterns = [
    path('api/v1/analytics/management-award/', ManagementAwardView.as_view()),
    path('api/v1/analytics/popug-with-negative-award-count/', PopugWithNegativeAwardCount.as_view()),
    path('api/v1/analytics/most-expansive-task/', MostExpensiveTaskView.as_view()),
]
