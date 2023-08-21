from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveRequestStatusUpdateSerializer, LeaveUpdateSerializer, WorkAllocationdisplaySerializer
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

class LeaveUpdateAPIView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveUpdateSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to update this leave.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class UserLeaveRequestListAPIView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user)

class UserLeaveDeshbordRequestListAPIView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user,status='accept')

class LeaveRequestStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

from django.shortcuts import get_object_or_404
class LeaveDeleteAPIView(APIView):
    def delete(self, request, pk):
        leave = get_object_or_404(LeaveRequest, pk=pk)
        if leave.user != request.user:
            return Response({'detail': 'You do not have permission to delete this leave.'}, status=status.HTTP_403_FORBIDDEN)
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
# class LeaveUserRequestCountView(APIView):
#     def get(self, request, format=None):
#         leave_request_count = LeaveRequest.objects.values('user').annotate(count=Count('user')).count()
#         return Response({'leave_request_count': leave_request_count})
    
class UserAcceptedLeaveListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        accepted_leaves = LeaveRequest.objects.filter(user=user, status='accept')
        total_accepted_leaves = accepted_leaves.count()  # Count the total number of accepted leaves
        serializer = LeaveRequestStatusUpdateSerializer(accepted_leaves, many=True)
        return Response({'total_accepted_leaves': total_accepted_leaves, 'leave_requests': serializer.data}, status=status.HTTP_200_OK)
    
from .models import WorkAllocation
from .serializers import WorkAllocationSerializer
from rest_framework.generics import CreateAPIView
from account.utils import create_log_entry
class CreateWorkAllocationView(CreateAPIView):
    serializer_class = WorkAllocationSerializer
    def create(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user_allocation = WorkAllocation.objects.get(user_id=user_id)
        except WorkAllocation.DoesNotExist:
            # Create a new WorkAllocation instance for the user
            user_allocation = WorkAllocation(user_id=user_id)
        serializer = self.get_serializer(user_allocation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            action = f"Created/Updated WorkAllocation for User ID: {user_id}"
            create_log_entry(request.user, action)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserWorkAllocationView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        work_allocations = WorkAllocation.objects.filter(user=user)
        serializer = WorkAllocationSerializer(work_allocations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkAllocationListView(generics.ListAPIView):
    queryset = WorkAllocation.objects.all()
    serializer_class = WorkAllocationdisplaySerializer


class WorkAllocationDetailView(generics.DestroyAPIView):
    queryset = WorkAllocation.objects.all()
    serializer_class = WorkAllocationdisplaySerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)