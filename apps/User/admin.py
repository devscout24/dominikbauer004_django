from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.location.models import Location
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q

class LocationInline(admin.TabularInline):
    model = Location
    fields = ["address"]
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [LocationInline]

    # Different list displays for different views
    list_display = (
        'customer_number', 'company_name', 'email', 'phone',
        'status_badge', 'is_active', 'is_staff', 'created_at', 'admin_actions'
    )
    
    list_filter = ('status', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    
    fieldsets = (
        (None, {
            'fields': (
                'customer_number', 'company_name', 'name',
                'email', 'phone', 'billing_location', 'password', 'status'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'customer_number','company_name','name','email',
                'phone','billing_location','password1','password2',
                'is_active','is_staff','is_superuser',
                'groups','user_permissions',
            ),
        }),
    )

    search_fields = ('customer_number','company_name','email','phone')
    ordering = ('-created_at',)

    # Custom methods
    def status_badge(self, obj):
        colors = {
            'new': 'warning',      # Yellow for new users
            'active': 'success',   # Green for active users  
            'inactive': 'secondary' # Gray for inactive
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def admin_actions(self, obj):
        if obj.status == 'new':
            # Use the correct admin URL pattern
            change_url = reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=[obj.id])
            return format_html(
                '<a href="{}" class="button" style="background: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Activate User</a>',
                change_url
            )
        elif obj.status == 'active':
            return format_html(
                '<span class="badge badge-success">✓ Active</span>'
            )
        return "-"
    admin_actions.short_description = 'Actions'

    # Custom actions
    actions = ['activate_selected_users', 'deactivate_users', 'move_to_new']

    def activate_selected_users(self, request, queryset):
        # Only activate users who are in 'new' status
        users_to_activate = queryset.filter(status='new')
        updated = users_to_activate.update(status='active', is_active=True)
        
        if updated > 0:
            self.message_user(request, f'{updated} users activated successfully and moved to Custom Users.')
        else:
            self.message_user(request, 'No new users selected for activation.', level=messages.WARNING)
    activate_selected_users.short_description = "✅ Activate selected NEW users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(status='inactive', is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
    deactivate_users.short_description = "❌ Deactivate selected users"

    def move_to_new(self, request, queryset):
        updated = queryset.update(status='new', is_active=False)
        self.message_user(request, f'{updated} users moved to New Users section.')
    move_to_new.short_description = "🆕 Move to New Users"

    # Custom URLs for different sections
    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        custom_urls = [
            path('new-users/', self.admin_site.admin_view(self.new_users_view), name='accounts_customuser_new'),
            path('custom-users/', self.admin_site.admin_view(self.custom_users_view), name='accounts_customuser_custom'),
        ]
        return custom_urls + urls

    def new_users_view(self, request):
        # Redirect to filtered view for new users
        url = reverse('admin:accounts_customuser_changelist') + '?status__exact=new'
        return HttpResponseRedirect(url)

    def custom_users_view(self, request):
        # Redirect to filtered view for active users
        url = reverse('admin:accounts_customuser_changelist') + '?status__exact=active'
        return HttpResponseRedirect(url)

    # Override changelist to show custom titles and counts
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        
        # Get status counts for sidebar
        status_counts = CustomUser.objects.aggregate(
            total=Count('id'),
            new=Count('id', filter=Q(status='new')),
            active=Count('id', filter=Q(status='active')),
            inactive=Count('id', filter=Q(status='inactive')),
        )
        
        extra_context['status_counts'] = status_counts
        
        # Set custom titles based on filter
        status_filter = request.GET.get('status__exact')
        if status_filter == 'new':
            extra_context['title'] = 'New Users - Pending Activation'
            extra_context['subtitle'] = f'{status_counts["new"]} users waiting for activation'
        elif status_filter == 'active':
            extra_context['title'] = 'Custom Users - Active Users'
            extra_context['subtitle'] = f'{status_counts["active"]} active users'
        else:
            extra_context['title'] = 'All Users'
            extra_context['subtitle'] = f'Total: {status_counts["total"]} users'
        
        return super().changelist_view(request, extra_context=extra_context)

    # Handle form submission - auto activate when password is set
    def save_model(self, request, obj, form, change):
        is_new = not change  # Check if this is a new object
        
        # If password is being set/changed and user is new, auto-activate
        if change and 'password' in form.changed_data and obj.status == 'new':
            obj.status = 'active'
            obj.is_active = True
            messages.success(request, f'User {obj.customer_number} activated successfully and moved to Custom Users.')
        
        # If creating new user via admin, set status to new
        if is_new:
            obj.status = 'new'
            obj.is_active = False
            
        super().save_model(request, obj, form, change)

    # Custom queryset to handle different views
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

# Admin site configuration
admin.site.site_header = "PUCEST Admin"
admin.site.site_title = "PUCEST Admin Portal"
admin.site.index_title = "Welcome to the PUCEST Admin Portal"