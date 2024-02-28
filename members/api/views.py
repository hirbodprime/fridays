from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import datetime
from django.utils import timezone
from members.models import Class, Attendance, Wallet
# Make sure to import Wallet model if you're using it for charging/refunding

from .serializers import ClassSerializer, AttendanceSerializer

class ClassViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()

class ToggleAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

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
