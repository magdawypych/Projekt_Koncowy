from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)


class Position(models.Model):
    POSITIONS = (
        (1, 'Technician'),
        (2, 'Laboratory Assistant'),
        (3, 'Laboratory Scientist'),
        (4, 'Research and Development Scientist')
    )
    position = models.IntegerField(choices=POSITIONS)


class Method(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    measurement_name = models.CharField(max_length=64, null=True)
    measurement_unit = models. CharField(max_length=64, null=True)
    realised_date = models.DateTimeField(auto_now=True)
    edition_date = models.DateTimeField(null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    procedure = models.TextField()


class Sample(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    analysis_date = models.DateField(auto_now=True)
    methods = models.ManyToManyField(Method, through='Analysis')


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_analysis = models.DateTimeField()
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    comments = models.TextField()
    result = models.IntegerField()


class Analysis(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    result = models.OneToOneField(Result, on_delete=models.CASCADE,  null=True)

