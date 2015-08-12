from rest_framework import serializers
from rbmo.models import PerformanceReport

class PerformanceReportSerializer(serializers.ModelSerializer):
    activity = serializers.StringRelatedField()

    class Meta:
        model = PerformanceReport
        fields = ('id','activity', 'month', 'year', 'received', 'incurred', 'remarks')
