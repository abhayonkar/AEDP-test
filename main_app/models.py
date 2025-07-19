# abhayonkar/aedp-test/AEDP-test-0557ce3e060e3a4334b3e58f088fa172e03244e4/main_app/models.py
from django.db import models
from django.contrib.auth.models import User

# Choices for various fields
YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

DEGREE_CHOICES = [
        ('B.Com', 'B.Com'),
        ('B.A.', 'B.A.'),
        ('B.Sc.', 'B.Sc.'),
        ('B.M.S.', 'B.M.S.'),
        ('B.Tech', 'B.Tech'),
        ('B.B.A.', 'B.B.A.'),
        ('Others', 'Others')
    ]

DURATION_CHOICES = [
    ('3-Year UG', '3-Year UG'),
    ('4-Year UG', '4-Year UG'),
]

# Basic Information Model
class BasicInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_name = models.CharField(max_length=255)
    pvc_name = models.CharField(max_length=255)
    report_date = models.DateField()
    academic_year = models.CharField(max_length=9)
    district = models.CharField(max_length=100)
    aishe_code = models.CharField(max_length=20, blank=True, null=True) # Added AISHE Code

    def __str__(self):
        return self.university_name

    class Meta:
        verbose_name = "Basic Information"
        verbose_name_plural = "Basic Information"

# Industry Model
class Industry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    industry_name = models.CharField(max_length=255)
    sector_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    curriculum_consulted_to_industry = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    aedp_programme = models.CharField(max_length=255)
    start_date = models.DateField()
    validity_date = models.DateField()
    student_commitment = models.IntegerField()
    stipend_range = models.CharField(max_length=255)
    type_of_engagement = models.TextField()
    contact_person = models.TextField()
    location_head = models.CharField(max_length=255)
    other_locations = models.TextField(blank=True, null=True)
    other_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.industry_name

    class Meta:
        verbose_name = "Industry Engagement"
        verbose_name_plural = "Industry Engagements"
        # Adjusted ordering based on forms.py to avoid inconsistencies
        ordering = ['curriculum_consulted_to_industry', 'location_head', 'other_locations']

# SSC (Sector Skill Council) Model
class SSC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ssc_name = models.CharField(max_length=255)
    sector_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    start_date = models.DateField()
    validity_date = models.DateField()
    aedp_programme = models.CharField(max_length=255)
    type_of_engagement = models.TextField()
    contact_person = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ssc_name

    class Meta:
        verbose_name = "Sector Skill Council (SSC)"
        verbose_name_plural = "Sector Skill Councils (SSC)"

# BOAT (Board of Apprenticeship Training) Model
class BOAT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus_college_name = models.CharField(max_length=255)
    mou_signed = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    aedp_programme = models.CharField(max_length=255)
    no_of_students = models.IntegerField()
    stipend = models.CharField(max_length=255)
    other_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.campus_college_name

    class Meta:
        verbose_name = "Board of Apprenticeship Training (BOAT)"
        verbose_name_plural = "Board of Apprenticeship Training (BOAT)"

# Program Model
class Program(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program_name = models.CharField(max_length=100, choices=DEGREE_CHOICES)
    other_degree = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    curriculum_file = models.FileField(upload_to='curriculum_files/', blank=True, null=True)
    syllabus_preparation = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    credit_allocation = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    board_of_deans_approval = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    academic_council_approval = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    timeline = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # New fields for Curriculum Structure checkboxes
    major_minor_multidisciplinary_course = models.BooleanField(default=False)
    skill_enhancement_course = models.BooleanField(default=False)
    ability_enhancement_course = models.BooleanField(default=False)
    value_added_course = models.BooleanField(default=False)
    apprenticeship_course = models.BooleanField(default=False)
    num_curriculum_ticks = models.IntegerField(default=0) # Field to store the count

    def __str__(self):
        return self.program_name

    class Meta:
        verbose_name = "Program Details"
        verbose_name_plural = "Program Details"

# Campus Model
class Campus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus_college_name = models.CharField(max_length=255)
    aedp_programme = models.CharField(max_length=255, blank=True, null=True) # Made nullable as per migration
    sector_name = models.CharField(max_length=255, blank=True, null=True) # Added sector name
    curriculum_type = models.TextField()
    same_aedp_continued = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    existing_degree_converted = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    faculty_department = models.CharField(max_length=255)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    apprenticeship_integration = models.TextField()
    student_intake = models.IntegerField()
    student_enrolled = models.IntegerField()
    industry_partners = models.TextField()

    def __str__(self):
        return self.campus_college_name

    class Meta:
        verbose_name = "Campus Details"
        verbose_name_plural = "Campus Details"

# Outreach Model
class Outreach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nodal_officer_orientation = models.CharField(max_length=255)
    faculty_workshops = models.IntegerField()
    industry_workshops = models.IntegerField()
    district_outreach_programs = models.IntegerField()
    parent_orientation = models.IntegerField()
    autonomous_colleges_onboarded = models.IntegerField()

    def __str__(self):
        return f"Outreach for {self.user.username}"

    class Meta:
        verbose_name = "Outreach Activity"
        verbose_name_plural = "Outreach Activities"

# Challenges Model
class Challenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Challenges for {self.user.username}"

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

# Timelines Model
class Timelines(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum_finalization = models.CharField(max_length=255)
    mou_execution = models.CharField(max_length=255)
    internal_approvals = models.CharField(max_length=255)
    faculty_orientation = models.CharField(max_length=255)
    admission_campaign_launch = models.CharField(max_length=255)
    student_enrollment_begin = models.CharField(max_length=255)
    program_commencement = models.CharField(max_length=255)
    monthly_progress_reporting = models.CharField(max_length=255)

    def __str__(self):
        return f"Timelines for {self.user.username}"

    class Meta:
        verbose_name = "Timeline"
        verbose_name_plural = "Timelines"