from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, BasicInfo, Industry, SSC, BOAT, Program, Campus, 
    Outreach, Challenges, Timelines
)

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Define a new User admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# You can still register other models if you want direct admin access to them
admin.site.register(BasicInfo)
admin.site.register(Industry)
admin.site.register(SSC)
admin.site.register(BOAT)
admin.site.register(Program)
admin.site.register(Campus)
admin.site.register(Outreach)
admin.site.register(Challenges)
admin.site.register(Timelines)
