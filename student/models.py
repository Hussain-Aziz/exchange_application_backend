from django.db import models

# Create your models here.
class Test(models.Model):
    test = models.CharField(max_length=100)

# seed data
    # Test.objects.create(test='test1')