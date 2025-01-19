from rest_framework import serializers
from ..models.network_coverage import NetworkCoverage


class NetworkCoverageSerializer(serializers.ModelSerializer):
    operator = serializers.CharField()
    x_lp93 = serializers.IntegerField()
    y_lp93 = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    g2 = serializers.BooleanField()  # 2G column
    g3 = serializers.BooleanField()  # 3G column
    g4 = serializers.BooleanField()  # 4G column
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = NetworkCoverage
        fields = '__all__'
