from django.contrib import admin
from .models import User
from .forms import UserCreationForm


class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm


admin.site.register(User, UserAdmin)
