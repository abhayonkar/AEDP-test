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
    DISTRICT_CHOICES = [
        ('Ahmednagar', 'Ahmednagar'),
        ('Akola', 'Akola'),
        ('Amravati', 'Amravati'),
        ('Aurangabad (Chhatrapati Sambhajinagar)', 'Aurangabad (Chhatrapati Sambhajinagar)'),
        ('Beed', 'Beed'),
        ('Bhandara', 'Bhandara'),
        ('Buldhana', 'Buldhana'),
        ('Chandrapur', 'Chandrapur'),
        ('Dhule', 'Dhule'),
        ('Gadchiroli', 'Gadchiroli'),
        ('Gondia', 'Gondia'),
        ('Hingoli', 'Hingoli'),
        ('Jalgaon', 'Jalgaon'),
        ('Jalna', 'Jalna'),
        ('Kolhapur', 'Kolhapur'),
        ('Latur', 'Latur'),
        ('Mumbai City', 'Mumbai City'),
        ('Mumbai Suburban', 'Mumbai Suburban'),
        ('Nagpur', 'Nagpur'),
        ('Nanded', 'Nanded'),
        ('Nandurbar', 'Nandurbar'),
        ('Nashik', 'Nashik'),
        ('Osmanabad', 'Osmanabad'),
        ('Palghar', 'Palghar'),
        ('Parbhani', 'Parbhani'),
        ('Pune', 'Pune'),
        ('Raigad', 'Raigad'),
        ('Ratnagiri', 'Ratnagiri'),
        ('Sangli', 'Sangli'),
        ('Satara', 'Satara'),
        ('Sindhudurg', 'Sindhudurg'),
        ('Solapur', 'Solapur'),
        ('Thane', 'Thane'),
        ('Wardha', 'Wardha'),
        ('Washim', 'Washim'),
        ('Yavatmal', 'Yavatmal'),
    ]

    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="District"
    )
    aishe_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="AISHE Code"
    )

    class Meta:
        model = BasicInfo
        fields = ['university_name', 'pvc_name', 'report_date', 'academic_year', 'district', 'aishe_code']
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
        fields = [
            'industry_name', 'sector_name', 'mou_signed', 'curriculum_consulted_to_industry',
            'aedp_programme', 'start_date', 'validity_date',
            'student_commitment', 'stipend_range', 'type_of_engagement',
            'contact_person', 'location_head', 'other_locations', 'other_details'
        ]
        # Added ordering to the Meta class
        # This will ensure that the fields are displayed in the specified order in the form
        ordering = ['curriculum_consulted_to_industry','location_head', 'other_locations'] 
        widgets = {
            'industry_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sector_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mou_signed': forms.Select(attrs={'class': 'form-select'}),
            'curriculum_consulted_to_industry': forms.Select(attrs={'class': 'form-select'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'validity_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'student_commitment': forms.NumberInput(attrs={'class': 'form-control'}),
            'stipend_range': forms.TextInput(attrs={'class': 'form-control'}),
            'type_of_engagement': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location_head': forms.TextInput(attrs={'class': 'form-control'}),
            'other_locations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'validity_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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
            'no_of_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'stipend': forms.TextInput(attrs={'class': 'form-control'}),
            'other_information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['user']
        widgets = {
            'program_name': forms.Select(attrs={'class': 'form-select'}),
            'other_degree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please specify the degree'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter specialization/branch'
            }),
            'curriculum_file': forms.FileInput(attrs={'class': 'form-control'}),
            'syllabus_preparation': forms.Select(attrs={'class': 'form-select'}),
            'credit_allocation': forms.Select(attrs={'class': 'form-select'}),
            'board_of_deans_approval': forms.Select(attrs={'class': 'form-select'}),
            'academic_council_approval': forms.Select(attrs={'class': 'form-select'}),
            'timeline': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the other_degree field appear only when 'Others' is selected
        self.fields['other_degree'].widget.attrs['style'] = 'display: none;'
class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        exclude = ['user']
        widgets = {
            'campus_college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'aedp_programme': forms.TextInput(attrs={'class': 'form-control'}),
            'sector_name': forms.TextInput(attrs={'class': 'form-control'}), # This line was added
            'curriculum_type': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'same_aedp_continued': forms.Select(attrs={'class': 'form-select'}),
            'existing_degree_converted': forms.Select(attrs={'class': 'form-select'}),
            'faculty_department': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'apprenticeship_integration': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'student_intake': forms.NumberInput(attrs={'class': 'form-control'}),
            'student_enrolled': forms.NumberInput(attrs={'class': 'form-control'}),
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
