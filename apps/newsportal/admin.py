from django.contrib import admin
from .models import NewsPortal
# Register your models here.

@admin.register(NewsPortal)
class NewsPortalAdmin(admin.ModelAdmin):
    list_display= ['title', 'issue_number', 'issue_date','banner', 'pdf_file', 'created_by','created_at','updated_at']
    search_fields= ['title', 'issue_number',"created_by"]
    list_filter= ["issue_number"]
    
    readonly_fields= ["created_at"]
    
