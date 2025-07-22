from django.db import models


from users.models import User

class FeedbackTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, choices=[('bug', 'Bug'), ('suggestion', 'Suggestion'), ('payment', 'Payment')])
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('open', 'Open'), ('resolved', 'Resolved')], default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
