from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
        ('import', 'Import'),
        ('export', 'Export'),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=50)
    object_uid = models.CharField(max_length=100)
    object_repr = models.TextField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} {self.user} {self.action} {self.object_type} {self.object_uid}"
