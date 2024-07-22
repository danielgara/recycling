from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    experience_points = models.IntegerField(default=0)


class Ranking(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()
    from_points = models.PositiveIntegerField()
    to_points = models.PositiveIntegerField()
    image = models.ImageField(upload_to='rankings_images/', blank=True, null=True)

    def __str__(self):
        return str(self.level) + ' - ' + self.name


class Code(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    id_physical_location = models.CharField(max_length=100)
    consecutive = models.PositiveIntegerField()
    id_container = models.PositiveIntegerField()
    id_model = models.CharField(max_length=100)
    material = models.PositiveIntegerField()
    success = models.IntegerField(choices=[(0, 'Failure'), (1, 'Success')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user.username) + ' - ' + str(self.id_physical_location)


class UserHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type_of_activity = models.CharField(max_length=50, choices=[('QR_SCAN', 'QR Scan')])
    accumulated_points = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user) + ' - ' + str(self.accumulated_points)


class Waste(models.Model):
    iteration = models.IntegerField()
    date = models.DateTimeField()
    name_ima_before = models.CharField(max_length=255)
    name_ima_after = models.CharField(max_length=255)
    mode = models.IntegerField()
    folder = models.CharField(max_length=255)
    res = models.IntegerField()
    rec = models.IntegerField()
    ecological_point = models.CharField(max_length=255)
    model_version = models.CharField(max_length=255)
    success = models.IntegerField()

    def __str__(self):
        return f"Iteration {self.iteration} - {self.date}"
