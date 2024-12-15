from rest_framework import serializers

from callboard.models import Ad, Feedback


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer(source='ad', read_only=True, many=True)

    class Meta:
        model = Feedback
        fields = '__all__'
