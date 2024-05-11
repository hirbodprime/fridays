from rest_framework import serializers
from django.contrib.auth import get_user_model
from members.models import Wallet, PaymentImage
from django.conf import settings


User = get_user_model()
class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['profile_image']
    def get_profile_image(self, obj):
        if obj.profile_image:
            return f"https://hirbots.com/fridays{obj.profile_image.url}"
        return None
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'profile_image')

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image:
            return f"https://hirbots.com/fridays{obj.profile_image.url}"
        return None
    class Meta:
        model = User
        fields = ['id','username', 'full_name', 'profile_image', 'join_date', 'premium']



class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user', 'balance']
        
class PaymentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentImage
        fields = ['id', 'image', 'amount', 'created_at']