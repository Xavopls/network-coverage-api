from django.db import models


class NetworkCoverage(models.Model):
    id = models.AutoField(primary_key=True)
    operator = models.CharField()
    x_lp93 = models.IntegerField()
    y_lp93 = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    g2 = models.BooleanField()  # 2G column
    g3 = models.BooleanField()  # 3G column
    g4 = models.BooleanField()  # 4G column
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "network_coverage"
