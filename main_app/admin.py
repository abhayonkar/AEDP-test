# abhayonkar/aedp-test/AEDP-test-0557ce3e060e3a4334b3e58f088fa172e03244e4/main_app/admin.py
from django.contrib import admin
from django.contrib.auth.models import User # Keep User imported
from django.urls import reverse # Import reverse for curriculum_download
from .models import (
    BasicInfo, Industry, SSC, BOAT, Program, Campus,
    Outreach, Challenges, Timelines
)

from django.utils.html import format_html


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'other_degree', 'specialization', 'curriculum_download', 'num_curriculum_ticks'] # Added other_degree and num_curriculum_ticks for display
    search_fields = ['program_name', 'other_degree', 'specialization'] # Added other_degree for search

    def curriculum_download(self, obj):
        if obj.curriculum_file:
            # Ensure 'download_curriculum' URL name exists in your urls.py
            return format_html(
                '<a href="{}" class="button" target="_blank">Download Curriculum</a>',
                reverse('download_curriculum', args=[obj.id])
            )
        return "No file available"
    curriculum_download.short_description = 'Curriculum'


# The User model is already registered by Django's auth app,
# so we remove the explicit registration here to avoid AlreadyRegistered exception.
# admin.site.register(User) # THIS LINE IS REMOVED

admin.site.register(BasicInfo)
admin.site.register(Industry)
admin.site.register(SSC)
admin.site.register(BOAT)
admin.site.register(Program, ProgramAdmin) # Register Program with ProgramAdmin
admin.site.register(Campus)
admin.site.register(Outreach)
admin.site.register(Challenges)
admin.site.register(Timelines)