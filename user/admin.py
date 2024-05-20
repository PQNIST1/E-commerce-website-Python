from django.contrib import admin
from .models import UserAccount
admin.site.register(UserAccount) # Dùng UserAccount thay vì User
# Register your models here.
