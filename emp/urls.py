from django.urls import path
from .views import LeaveRequestListCreateAPIView, LeaveRequestStatusUpdateAPIView, LeaveCountAPIView, TotalleaveCountAPIView, UserAcceptedLeaveListView, WorkAllocationListView
from .views import UserLeaveRequestListAPIView, UserLeaveDeshbordRequestListAPIView, LeaveDeleteAPIView, LeaveUpdateAPIView, CreateWorkAllocationView, UserWorkAllocationView, WorkAllocationDetailView
from . import views


app_name = 'emp'

urlpatterns = [

    path('empleave/',views.empleave,name='empleave'),


    # Api
    path('leave-create/', LeaveRequestListCreateAPIView.as_view(), name='leave-request-create'),
    path('leave-delete/<int:pk>/', LeaveDeleteAPIView.as_view(), name='leave-delete'),
    path('leavetiming-update/<int:pk>/', LeaveUpdateAPIView.as_view(), name='leave-update'),
    path('user-leave-info/', UserLeaveRequestListAPIView.as_view(), name='leave-info'),
    path('user-leave-info-deshbord/', UserLeaveDeshbordRequestListAPIView.as_view(), name='leave-info-desh'),
    path('leave-update/<int:pk>/', LeaveRequestStatusUpdateAPIView.as_view(), name='leave-request-update-status'),
    path('accept-leave-count/', LeaveCountAPIView.as_view(), name='leave-count'),
    path('Total-leave-count/', TotalleaveCountAPIView.as_view(), name='totalleave-count'),
    # path('Totaluser-leave-request-count/', LeaveUserRequestCountView.as_view(), name='leave-request-count'), 
    path('loginuser-accepted-leaves/', UserAcceptedLeaveListView.as_view(), name='user-accepted-leaves'), #display the login user accepted leave
    path('work-allocate/<int:user_id>/', CreateWorkAllocationView.as_view(), name='create-work-allocation'),
    path('login-work-allocations/', UserWorkAllocationView.as_view(), name='user-work-allocations'),
    path('workallocations/', WorkAllocationListView.as_view(), name='workallocation-list'),
    path('workallocations/<int:pk>/', WorkAllocationDetailView.as_view(), name='workallocation-detail'),


]
