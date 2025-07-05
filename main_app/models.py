from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# -----------------------------------------------------------------------------
# USER PROFILE
# -----------------------------------------------------------------------------
class UserProfile(models.Model):
    """
    Extends the default Django User model to include a group (A or B).
    This is created automatically when a new User is created.
    """
    class Group(models.TextChoices):
        A = 'A', 'Group A'
        B = 'B', 'Group B'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    group = models.CharField(max_length=1, choices=Group.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Signal to create or update the user profile when a User object is saved."""
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


# -----------------------------------------------------------------------------
# SINGLE-ENTRY MODELS (One per user)
# -----------------------------------------------------------------------------
class BasicInfo(models.Model):
    """Stores the basic report information for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basic_info')
    university_name = models.CharField(max_length=255, default="Default University")
    pvc_name = models.CharField(max_length=255, default="Default PVC")
    report_date = models.DateField(default=date.today)
    academic_year = models.CharField(max_length=10, default="2024-25")

    def __str__(self):
        return f"Basic Info for {self.user.username}"

class Outreach(models.Model):
    """Stores the outreach and stakeholder engagement data for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='outreach')
    nodal_officer_orientation = models.CharField(max_length=255, blank=True)
    faculty_workshops = models.PositiveIntegerField(default=0)
    industry_workshops = models.PositiveIntegerField(default=0)
    district_outreach_programs = models.PositiveIntegerField(default=0)
    parent_orientation = models.PositiveIntegerField(default=0)
    autonomous_colleges_onboarded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Outreach Data for {self.user.username}"

class Challenges(models.Model):
    """Stores the challenges and risk mitigation strategy for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='challenges')
    content = models.TextField(blank=True)

    def __str__(self):
        return f"Challenges for {self.user.username}"

class Timelines(models.Model):
    """Stores the timeline data for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='timelines')
    curriculum_finalization = models.CharField(max_length=255, blank=True)
    mou_execution = models.CharField(max_length=255, blank=True)
    internal_approvals = models.CharField(max_length=255, blank=True)
    faculty_orientation = models.CharField(max_length=255, blank=True)
    admission_campaign_launch = models.CharField(max_length=255, blank=True)
    student_enrollment_begin = models.CharField(max_length=255, blank=True)
    program_commencement = models.CharField(max_length=255, blank=True)
    monthly_progress_reporting = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Timelines for {self.user.username}"

# -----------------------------------------------------------------------------
# MULTI-ENTRY MODELS (Many per user)
# -----------------------------------------------------------------------------
class Industry(models.Model):
    """Stores an industry engagement entry. A user can have multiple."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='industry_entries')
    industry_name = models.CharField(max_length=255)
    sector_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    type_of_engagement = models.CharField(max_length=255)
    contact_person = models.TextField()
    location = models.CharField(max_length=255)
    aedp_programme = models.CharField(max_length=255)
    other_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.industry_name} for {self.user.username}"

class SSC(models.Model):
    """Stores a Sector Skill Council (SSC) entry. A user can have multiple."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ssc_entries')
    ssc_name = models.CharField(max_length=255)
    sector_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    aedp_programme = models.CharField(max_length=255)
    type_of_engagement = models.TextField()
    contact_person = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ssc_name} for {self.user.username}"

class BOAT(models.Model):
    """Stores a BOAT collaboration entry. A user can have multiple."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boat_entries')
    campus_college_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    aedp_programme = models.CharField(max_length=255)
    other_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.campus_college_name} BOAT entry for {self.user.username}"

class Program(models.Model):
    """Stores an AEDP program implementation progress entry. A user can have multiple."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_entries')
    program_name = models.CharField(max_length=255)
    component = models.CharField(max_length=100, choices=[
        ('Syllabus Preparation', 'Syllabus Preparation'),
        ('Credit Allocation', 'Credit Allocation'),
        ('Board of Deans Approval', 'Board of Deans Approval'),
        ('Academic Council Approval', 'Academic Council Approval')
    ])
    status = models.CharField(max_length=20, choices=[
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Not Started', 'Not Started')
    ])
    timeline = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.program_name} ({self.component}) for {self.user.username}"

class Campus(models.Model):
    """Stores a campus/college details entry. A user can have multiple."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campus_entries')
    campus_college_name = models.CharField(max_length=255)
    aedp_programme = models.CharField(max_length=255)
    curriculum_type = models.TextField()
    same_aedp_continued = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    existing_degree_converted = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    faculty_department = models.CharField(max_length=255)
    duration = models.CharField(max_length=20, choices=[('3-Year UG', '3-Year UG'), ('4-Year UG', '4-Year UG')])
    apprenticeship_integration = models.TextField()
    student_intake = models.PositiveIntegerField()
    industry_partners = models.TextField()

    def __str__(self):
        return f"{self.campus_college_name} campus entry for {self.user.username}"
