from rest_framework import serializers
from .models import UploadHistory

class UploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField()
    
class UploadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadHistory
        fields = ["id", "filename", "uploaded_at", "summary"]