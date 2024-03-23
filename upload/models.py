from django.db import models
from members.models import Class
# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    class_ref = models.ForeignKey(Class, related_name='videos', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title