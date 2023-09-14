from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


# for storing details of user given for prescription
class UserInputs(models.Model):
    phone_number = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=10)
    work_condition = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    age = models.IntegerField()
    image = models.ImageField(upload_to='user_inputs')

    date = models.DateField
    time = models.TimeField