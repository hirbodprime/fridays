from django.contrib import admin
from members.models import Class, Attendance

admin.site.register(Class)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_attended', 'status', 'timestamp')  # Customize the columns displayed
    list_filter = ('status', 'timestamp')  # Enable filtering by status and timestamp
    search_fields = ('user__username', 'class_attended__title')  # Enable search by user and class title

admin.site.register(Attendance, AttendanceAdmin)
