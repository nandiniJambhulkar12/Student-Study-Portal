# from django.contrib import admin
# from . models import *
# # Register your models here.
# admin.site.register(Notes)

from django.contrib import admin
from .models import Notes ,Homework ,Todo # Explicitly import Notes

# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)