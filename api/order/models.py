from django.db import models
from django.conf import settings
# Create your models here.
class Trash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact = models.CharField(max_length=14)
    location = models.CharField(max_length=250)
    take_out_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'trash'
        verbose_name_plural = 'trashes'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.take_out_date} "