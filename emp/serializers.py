from rest_framework import serializers
from .models import LeaveRequest
from account.models import CustomUser

class LeaveRequestSerializer(serializers.ModelSerializer):
    user= serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = LeaveRequest
        fields = ('id', 'user', 'from_date', 'to_date', 'status', 'reason')
        read_only_fields = ('user', 'status')
    def validate(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        if not from_date:
            raise serializers.ValidationError({"From Date": ["This field is required."]})
        if not to_date:
            raise serializers.ValidationError({"To Date": ["This field is required."]})
        if from_date > to_date:
            raise serializers.ValidationError("From date must be before to date.")
        user = self.context['request'].user
        overlapping_leave = LeaveRequest.objects.filter(
            user=user,
            from_date__lte=to_date,
            to_date__gte=from_date
        ).exclude(pk=self.instance.pk if self.instance else None)
        if overlapping_leave.exists():
            raise serializers.ValidationError("For that perticulr date range the leave is already present .")
        return data

class LeaveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('from_date', 'to_date')


class LeaveCountSerializer(serializers.Serializer):
    user = serializers.CharField()
    leave_count = serializers.IntegerField()

class LeaveRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('status',)