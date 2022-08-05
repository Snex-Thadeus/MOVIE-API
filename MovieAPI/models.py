from django.db import models


class Movies(models.Model):
    Movie_Rank = models.AutoField(primary_key=True)
    Movie_Name = models.CharField(max_length=200)
    Year_of_Release = models.IntegerField()
    Movie_Rating = models.DecimalField(max_digits = 5, decimal_places = 2)
    Movie_Duration = models.DurationField()
    Movie_Description = models.CharField(max_length=1000)
    Date_Time = models.DateTimeField()
