from rest_framework import serializers
from .models import FeedbackTicket

class FeedbackTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackTicket
        fields = '__all__'
