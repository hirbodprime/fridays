from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

class Class(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    charge_amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_available_this_week = models.BooleanField(default=True)  # New field
    image = models.ImageField(upload_to="class/images",null=True,blank=True)
    def __str__(self):
        return self.title

    # @property
    # def is_this_week(self):
    #     today = timezone.now().date()
    #     start_week = today - datetime.timedelta(days=today.weekday())
    #     end_week = start_week + datetime.timedelta(days=6)
    #     return start_week <= self.date <= end_week

    class Meta:
        verbose_name_plural = "classes"

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('present', 'Present'), ('absent', 'Absent')))
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.class_attended} - {self.status}"

        
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user}'s wallet balance: {self.balance}"

    def charge(self, amount):
        if self.balance < amount:
            raise ValueError('Insufficient balance in wallet.')
        self.balance -= amount
        self.save()

    def add_funds(self, amount):
        """Add funds to the wallet."""
        self.balance += amount
        self.save()

    def subtract_funds(self, amount):
        """Subtract funds from the wallet, ensuring balance does not become negative."""
        if self.balance < amount:
            raise ValueError('Insufficient balance to subtract.')
        self.balance -= amount
        self.save()


class PaymentImage(models.Model):
    image = models.ImageField(upload_to='payment_images/')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} made on {self.created_at}"
