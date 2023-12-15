from django.db import models
from cars.models import CarModel

# Create your models here.


class CommentModel(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    email = models.EmailField()
    car = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="comments")
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.email
