
from django.contrib import admin
from .models import EventCategory, Event, Hashtags
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
admin.site.site_header = 'Event Listing Admin Panel'
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_start_datetime', 'event_attendees', 'location', 'category', 'status')
    list_filter = ('category', 'status')
    search_fields = ('title', 'location')
    list_editable = ('status',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('category', 'user')
        return queryset

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['choices'] = [('1', 'Pending'), ('2', 'Approved'), ('3', 'Suspended')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     if change:
    #         # Check if the status field was modified
    #         if 'status' in form.changed_data:
    #             new_status = form.cleaned_data['status']
    #             if new_status == '1':
    #                 # Perform any necessary logic or updates based on the 'pending' status
    #                 pass  # No changes to event_attendees
    #             elif new_status == '2':
    #                 # Perform any necessary logic or updates based on the 'approved' status
    #                 pass  # No changes to event_attendees
    #             elif new_status == '3':
    #                 # Perform any necessary logic or updates based on the 'suspended' status
    #                 pass  # No changes to event_attendees

    #     obj.save()

admin.site.register(Event, EventAdmin)



class HashtagsAdmin(admin.ModelAdmin):
    list_display = ('hashtag_name', 'status')
    list_filter = ('status',)
    search_fields = ('hashtag_name',)
    list_editable = ('status',)  # Add this line to make the 'status' field editable in the list view

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs['choices'] = [('1', 'Pending'), ('2', 'Approved'), ('3', 'Suspended')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            # Update the status field based on the new value
            if obj.status == '2':
                # Perform any necessary logic or updates based on the 'Approved' status
                pass  # Example: Do something for 'Approved' status
            elif obj.status == '3':
                # Perform any necessary logic or updates based on the 'Suspended' status
                pass  # Example: Do something for 'Suspended' status

        obj.save()

admin.site.register(Hashtags, HashtagsAdmin)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('event_category', 'display_status_button')
    list_filter = ('status',)
    actions = ['toggle_status']

    def display_status_button(self, obj):
        button_text = 'Active' if obj.status == '1' else 'Inactive'
        button_color = 'green' if obj.status == '1' else 'red'
        button_html = f'<button type="button" style="background-color: {button_color}; color: white;" ' \
                      f'onclick="changeStatus({obj.pk})">{button_text}</button>'
        return format_html(button_html)

    display_status_button.short_description = 'Status'

    def toggle_status(self, request, queryset):
        # Toggle the status of selected EventCategory objects
        for category in queryset:
            category.status = '2' if category.status == '1' else '1'  # Toggle between 'active' and 'inactive'
            category.save()

    toggle_status.short_description = 'Toggle Status'

    class Media:
        js = ('admin/js/event_category_admin.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/change_status/', self.admin_site.admin_view(self.change_status_view), name='change-status'),
        ]
        return custom_urls + urls

    def change_status_view(self, request, pk):
        if request.method == 'POST':
            category = get_object_or_404(EventCategory, pk=pk)
            category.status = '2' if category.status == '1' else '1'  # Toggle between 'active' and 'inactive'
            category.save()

            response_data = {
                'success': True,
                'message': 'Status updated successfully.',
            }
            return JsonResponse(response_data)
        
