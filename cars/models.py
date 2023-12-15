from django.db import models

# Create your models here.


class BrandModel(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True)

    def __str__(self) -> str:
        return self.brand_name


class CarModel(models.Model):
    car_name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='cars/media/uploads/')
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.car_name
