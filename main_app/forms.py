from django import forms
from .models import (
    BasicInfo, Industry, SSC, BOAT, Program, Campus, Outreach, Challenges, Timelines
)

class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

# -----------------------------------------------------------------------------
# MODEL FORMS
# -----------------------------------------------------------------------------

class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = BasicInfo
        fields = ['university_name', 'pvc_name', 'report_date', 'academic_year']
        widgets = {
            'university_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pvc_name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
        }

class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        exclude = ['user']
        widgets = {
            'industry_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sector_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mou_signed': forms.Select(attrs={'class': 'form-select'}),
            'type_of_engagement': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'other_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SSCForm(forms.ModelForm):
    class Meta:
        model = SSC
        exclude = ['user']
        widgets = {
            'ssc_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sector_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mou_signed': forms.Select(attrs={'class': 'form-select'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_engagement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_person': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BOATForm(forms.ModelForm):
    class Meta:
        model = BOAT
        exclude = ['user']
        widgets = {
            'campus_college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mou_signed': forms.Select(attrs={'class': 'form-select'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'other_information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['user']
        widgets = {
            'program_name': forms.TextInput(attrs={'class': 'form-control'}),
            'component': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'timeline': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        exclude = ['user']
        widgets = {
            'campus_college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'curriculum_type': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'same_aedp_continued': forms.Select(attrs={'class': 'form-select'}),
            'existing_degree_converted': forms.Select(attrs={'class': 'form-select'}),
            'faculty_department': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'apprenticeship_integration': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'student_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'industry_partners': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OutreachForm(forms.ModelForm):
    class Meta:
        model = Outreach
        exclude = ['user']
        widgets = {
            'nodal_officer_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty_workshops': forms.NumberInput(attrs={'class': 'form-control'}),
            'industry_workshops': forms.NumberInput(attrs={'class': 'form-control'}),
            'district_outreach_programs': forms.NumberInput(attrs={'class': 'form-control'}),
            'parent_orientation': forms.NumberInput(attrs={'class': 'form-control'}),
            'autonomous_colleges_onboarded': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ChallengesForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class TimelinesForm(forms.ModelForm):
    class Meta:
        model = Timelines
        exclude = ['user']
        widgets = {
            'curriculum_finalization': forms.TextInput(attrs={'class': 'form-control'}),
            'mou_execution': forms.TextInput(attrs={'class': 'form-control'}),
            'internal_approvals': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty_orientation': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_campaign_launch': forms.TextInput(attrs={'class': 'form-control'}),
            'student_enrollment_begin': forms.TextInput(attrs={'class': 'form-control'}),
            'program_commencement': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_progress_reporting': forms.TextInput(attrs={'class': 'form-control'}),
        }
