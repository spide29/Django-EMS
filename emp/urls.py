from django.urls import path
from .views import LeaveRequestListCreateAPIView, LeaveRequestStatusUpdateAPIView, LeaveCountAPIView, TotalleaveCountAPIView
from . import views


app_name = 'emp'

urlpatterns = [

    path('empleave/',views.empleave,name='empleave'),


    # Api
    path('leave-create/', LeaveRequestListCreateAPIView.as_view(), name='leave-request-create'),
    path('leave-update/<int:pk>/', LeaveRequestStatusUpdateAPIView.as_view(), name='leave-request-update-status'),
    path('accept-leave-count/', LeaveCountAPIView.as_view(), name='leave-count'),
    path('Total-leave-count/', TotalleaveCountAPIView.as_view(), name='totalleave-count'),

    
]
