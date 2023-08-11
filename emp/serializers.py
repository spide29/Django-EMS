from rest_framework import serializers
from .models import LeaveRequest
from account.models import CustomUser

class LeaveRequestSerializer(serializers.ModelSerializer):
    user= serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = LeaveRequest
        fields = ('id', 'user', 'from_date', 'to_date', 'status', 'reason')
        read_only_fields = ('user', 'status')

class LeaveCountSerializer(serializers.Serializer):
    user = serializers.CharField()
    leave_count = serializers.IntegerField()

class LeaveRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('status',)