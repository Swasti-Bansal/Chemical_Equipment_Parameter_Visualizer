from rest_framework import serializers
from .models import UploadHistory

class UploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField()
    
class UploadHistorySerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p", read_only=True)
    class Meta:
        model = UploadHistory
        fields = ["id", "filename", "uploaded_at", "summary"]