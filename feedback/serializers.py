from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']

    def create(self, validated_data):
        user = self.context['request'].user  # Access user from the request context
        return Feedback.objects.create(user=user, **validated_data)
