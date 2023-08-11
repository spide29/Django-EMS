from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveRequestStatusUpdateSerializer, LeaveCountSerializer
from rest_framework import generics

def empleave(request):
    access_token = request.COOKIES.get('access_token')
    context = {
        'access_token': access_token,
    }
    return render(request, 'employee/leaveform.html', context)







#####################################     API
class LeaveRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

class LeaveRequestStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

from django.db.models import Count
# class LeaveCountAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, *args, **kwargs):
#         leave_count_queryset = LeaveRequest.objects.filter(user=request.user).values('user__username').annotate(leave_count=Count('id'))
#         serializer = LeaveCountSerializer(leave_count_queryset, many=True)
#         return Response(serializer.data)

class TotalleaveCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        total_users = LeaveRequest.objects.count()
        return Response({"total_leave": total_users}, status=status.HTTP_200_OK)
class LeaveCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        accepted_leave_count = LeaveRequest.objects.filter(status='accept').count()
        return Response({"accepted_leave_count": accepted_leave_count}, status=status.HTTP_200_OK)