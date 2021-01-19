from django.db import models
from users.models import User

# Create your models here.
class Review(models.Model):
    STATUSES = [
        ('I', 'Init'),
        ('M', 'On moderation'),
        ('P', 'Published'),
        ('R', 'Rejected'),        
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUSES, default="I", max_length=20)