from django.db import models
from members.models import Class
from django.conf import settings

# Create your models here.
class Quote(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_ref = models.ForeignKey(Class, related_name='quotes', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_ref = models.ForeignKey(Class, related_name='comments', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)