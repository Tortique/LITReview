from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=168)
    image = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (250, 250)

    def resize_image(self):
        try:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)
        except Exception as e:
            print("no file found", e)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        unique_together = ("user", "followed_user",)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(user=models.F("followed_user")),
            ),
        ]
