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
from members.models import Class, Attendance, Wallet, PaymentImage
from account.models import CustomUser
# Make sure to import Wallet model if you're using it for charging/refunding
from .serializers import ClassSerializer, AttendanceSerializer,PaymentImageSerializer,UserSerializer

import decimal


class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.premium
class UpdateWalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Allow premium users to update the wallet balance of a specific user."""
        user = request.user
        
        # Ensure only premium users can access this feature
        if user.premium:
            try:
                # Retrieve the user for whom the wallet balance should be updated
                target_user = CustomUser.objects.get(id=user_id)

                # Retrieve the wallet for the target user, create one if it doesn't exist
                wallet, created = Wallet.objects.get_or_create(user=target_user)

                amount = request.data.get('amount')

                # Check if the amount is provided (allow 0 as valid)
                if amount is None:
                    return Response({'error': 'A valid amount is required.'}, status=400)

                # Ensure the amount is a valid decimal number
                try:
                    amount = decimal.Decimal(amount)
                except decimal.InvalidOperation:
                    return Response({'error': 'Amount must be a valid decimal number.'}, status=400)

                # Change the wallet balance for the target user
                wallet.change_fund(amount)

                return Response({
                    'success': True,
                    'balance': wallet.balance
                }, status=200)

            except CustomUser.DoesNotExist:
                return Response({
                    'success': False,
                    'error': f'User with ID {user_id} does not exist.'
                }, status=404)

            except Exception as e:
                return Response({
                    'success': False,
                    'error': str(e)
                }, status=400)
        else:
            return Response({
                'success': False,
                'error': 'Only premium users can update their wallet balance.'
            }, status=403)



class UserPaymentImageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return each user with their associated payment images, ordered by newest."""
        user = request.user
        
        if user.premium:
            # Get all users
            users = CustomUser.objects.all()
            users_data = []

            # Iterate through each user and collect their payment images
            for user in users:
                # Order payment images by 'created_at' field (newest first)
                payment_images = PaymentImage.objects.filter(user=user).order_by('-created_at')
                payment_image_serializer = PaymentImageSerializer(payment_images, many=True)
                user_serializer = UserSerializer(user)

                users_data.append({
                    'user': user_serializer.data,
                    'payment_images': payment_image_serializer.data
                })
            
            return Response({
                'success': True,
                'data': users_data
            }, status=200)
        else:
            return Response({
                'success': False,
                'error': 'You must be a premium user to access payment images.'
            }, status=403)

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
