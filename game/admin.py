from django.contrib import admin
from .models import details, scores 
# Register your models here.

class detailAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone')

class scoreAdmin(admin.ModelAdmin):
	list_display = ('user', 'score', 'win', 'date')

admin.site.register(details, detailAdmin)
admin.site.register(scores, scoreAdmin)