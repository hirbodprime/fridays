from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from account.models import InvitationCode  # Import the InvitationCode model
from .serializers import UserUpdateSerializer, UserProfileSerializer, WalletSerializer, PaymentImageSerializer, ProfilePictureSerializer
from members.models import Wallet, PaymentImage


User = get_user_model()


class UploadProfilePicture(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user  # Assuming the user is authenticated
        profile_image = request.data.get('profile_image')

        if not profile_image:
            return Response({'error': 'No profile image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user's profile image
        user.profile_image = profile_image
        user.save()

        # Serialize the updated profile image and return the response
        serializer = ProfilePictureSerializer(user)
        return Response(serializer.data)

    def get(self, request, format=None):
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            user = User.objects.get(
            username=username,
            )
            user_data = {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "join_date": user.join_date,
                "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
                "premium": user.premium
            }
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key,'user_data':user_data}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        full_name = request.data.get("full_name", None)
        invitation_code = request.data.get("invitation_code", None)  # Retrieve the invitation code from the request

        # Validate the invitation code
        if invitation_code is None or not InvitationCode.objects.filter(code=invitation_code).exists():
            return Response({"detail": "Invalid or missing invitation code."}, status=status.HTTP_400_BAD_REQUEST)

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the invitation code as used

        # Create the user
        user = User.objects.create(
            username=username,
            full_name=full_name,
            password=make_password(password)  # Ensure the password is hashed
            # Add additional fields here
        )
        user_data = {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "join_date": user.join_date,
            "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
            "premium": user.premium
            # Add any additional fields you wish to include in the response
        }
        # Create a token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token to the user
        return Response({"token": token.key,"user_data":user_data}, status=status.HTTP_201_CREATED)


class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Handle full updates to the user profile.
        """
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Handle partial updates to the user profile.
        """
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    """
    Retrieve a user profile by username.
    """
    
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        serializer = UserProfileSerializer(user)
        response_data = {
            'user_data':serializer.data
        }
        return Response(response_data)




class PaymentImageView(CreateAPIView):
    queryset = PaymentImage.objects.all()
    serializer_class = PaymentImageSerializer
    permission_classes = [IsAuthenticated]  # Optional, adjust according to your security requirements

class WalletAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)
        wallet = get_object_or_404(Wallet, user=user)
        serializer = WalletSerializer(wallet)
        response_data = {
            'user_data':serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
