from django.shortcuts import render
from cars import models


def home(request, brand=None):
    cars = models.CarModel.objects.all()
    brands = models.BrandModel.objects.all()
    if brand is not None:
        singleBrand = models.BrandModel.objects.get(slug=brand)
        cars = models.CarModel.objects.filter(brand=singleBrand)
    print(brand)
    return render(request, "home.html", {"brands": brands, "cars": cars})
