from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission
import datetime
from django.utils import timezone
from members.models import Class, Attendance, Wallet
# Make sure to import Wallet model if you're using it for charging/refunding

from .serializers import ClassSerializer, AttendanceSerializer



class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.premium

class ClassCreateAPIView(CreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsPremiumUser]

    def create(self, request, *args, **kwargs):
        if not request.user.premium:
            return Response({"detail": "Only premium users can create classes."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class ClassUpdateAPIView(UpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsPremiumUser]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        if not request.user.premium:
            return Response({"detail": "Only premium users can update classes."}, status=status.HTTP_403_FORBIDDEN)
        
        partial = kwargs.pop('partial', True)  # This allows partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class AttendedClassesListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ClassSerializer

    def get_queryset(self):
        """
        Override the get_queryset method to return only the classes
        that the current user has attended.
        """
        user = self.request.user
        attended_classes_ids = Attendance.objects.filter(user=user, status='present').values_list('class_attended', flat=True)
        return Class.objects.filter(id__in=attended_classes_ids, finished=True)

class ClassHistoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ClassSerializer

    def get_queryset(self):
        """
        Override the get_queryset method to return only the classes
        that are finished.
        """
        return Class.objects.filter(finished=True).order_by('-date')

class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = ClassSerializer

    def get_queryset(self):
        """
        Override the get_queryset method to return only the classes
        that are not finished.
        """
        return Class.objects.filter(finished=False)

class ToggleAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = request.user
        class_to_attend = get_object_or_404(Class, pk=pk)
        
        try:
            attendance = Attendance.objects.get(user=user, class_attended=class_to_attend)
            status_message = f'Your attendance status for this class is {attendance.status}.'
        except Attendance.DoesNotExist:
            status_message = 'You have not marked attendance for this class.'

        return Response({
            'attendance_status': attendance.status if 'attendance' in locals() else 'absent',
            'message': status_message
        }, status=status.HTTP_200_OK)
    @transaction.atomic
    def post(self, request, pk, format=None):
        user = request.user
        class_to_attend = get_object_or_404(Class, pk=pk)
        
        attendance, created = Attendance.objects.get_or_create(
            user=user,
            class_attended=class_to_attend,
            defaults={'status': 'absent'}
        )

        wallet, _ = Wallet.objects.get_or_create(user=user)
        
        if attendance.status == 'absent':
            attendance.status = 'present'
            wallet.add_funds(20)
        else:
            if attendance.status == 'present':
                attendance.status = 'absent'
                wallet.subtract_funds(20)

        attendance.save()
        wallet.save()  # Ensure the wallet changes are saved

        return Response({
            'attendance_status': attendance.status,
            'wallet_balance': wallet.balance,
            'message': f'Your attendance status has been updated to {attendance.status}, and your wallet has been adjusted.'
        }, status=status.HTTP_200_OK)
