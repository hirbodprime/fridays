from django.db import models
from account.models import CustomUser

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_users = models.ManyToManyField(CustomUser, related_name='tasks',blank=True)

    def __str__(self):
        return f"{self.title}, {self.id}"
