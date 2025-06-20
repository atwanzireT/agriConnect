from django.db import models
from accounts.models import User

# Create your models here.
class Feedback(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedback')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

