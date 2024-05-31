from django.contrib import admin
from .models import Trash
# Register your models here.

@admin.register(Trash)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['user','contact', 'location',
                    'take_out_date', 'created_at']
