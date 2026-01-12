from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLog(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=30, blank=True, null=True)    
    object_id = models.UUIDField(max_length=30, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    changes = models.CharField(max_length=255,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
