from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import *

# --- NEW IMPORTS for fpdf2 ---
from fpdf import FPDF, HTMLMixin

# -----------------------------------------------------------------------------
# PDF Generation Class using fpdf2 (Improved)
# -----------------------------------------------------------------------------
class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AEDP Implementation Status Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(4)

    def table(self, headers, data, col_widths):
        self.set_font('Arial', 'B', 8)
        # Header
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, 1, 0, 'C')
        self.ln()
        # Data
        self.set_font('Arial', '', 8)
        for row in data:
            # Check for page break before drawing a row
            if self.get_y() + 14 > self.h - self.b_margin: # 14 is approx height of a two-line row
                self.add_page()

            # Use a consistent height for all cells in a row
            max_lines = 1
            for i, item in enumerate(row):
                lines = self.multi_cell(col_widths[i], 5, str(item), 0, 'L', split_only=True)
                if len(lines) > max_lines:
                    max_lines = len(lines)
            
            row_height = 5 * max_lines
            x_start = self.get_x()
            for i, item in enumerate(row):
                self.multi_cell(col_widths[i], 5, str(item), 1, 'L')
                self.set_xy(self.get_x() + col_widths[i], self.get_y() - row_height)
            
            self.set_x(x_start) # Reset x position
            self.ln(row_height)


    def key_value_section(self, data_dict):
        self.set_font('Arial', '', 9)
        for key, value in data_dict.items():
            if self.get_y() + 7 > self.h - self.b_margin:
                self.add_page()
            self.set_font('Arial', 'B', 9)
            self.cell(70, 7, f"{key}:", 0, 0, 'L')
            self.set_font('Arial', '', 9)
            self.multi_cell(0, 7, str(value), 0, 'L')
        self.ln()

# -----------------------------------------------------------------------------
# AUTHENTICATION AND OTHER VIEWS (These are unchanged)
# -----------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
            else: messages.error(request, 'Invalid username or password.')
    else: form = LoginForm()
    return render(request, 'main_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        all_users = User.objects.filter(is_superuser=False)
        return render(request, 'main_app/admin_dashboard.html', {'all_users': all_users})
    else:
        basic_info, _ = BasicInfo.objects.get_or_create(user=request.user)
        outreach, _ = Outreach.objects.get_or_create(user=request.user)
        challenges, _ = Challenges.objects.get_or_create(user=request.user)
        timelines, _ = Timelines.objects.get_or_create(user=request.user)
        context = {
            'basic_info_form': BasicInfoForm(instance=basic_info),
            'outreach_form': OutreachForm(instance=outreach),
            'challenges_form': ChallengesForm(instance=challenges),
            'timelines_form': TimelinesForm(instance=timelines),
            'industry_form': IndustryForm(), 'ssc_form': SSCForm(), 'boat_form': BOATForm(),
            'program_form': ProgramForm(), 'campus_form': CampusForm(),
            'industry_entries': Industry.objects.filter(user=request.user),
            'ssc_entries': SSC.objects.filter(user=request.user),
            'boat_entries': BOAT.objects.filter(user=request.user),
            'program_entries': Program.objects.filter(user=request.user),
            'campus_entries': Campus.objects.filter(user=request.user),
        }
        return render(request, 'main_app/user_dashboard.html', context)

@login_required
def update_basic_info(request):
    instance = get_object_or_404(BasicInfo, user=request.user)
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, instance=instance)
        if form.is_valid(): form.save(); messages.success(request, 'Basic Information updated.')
    return redirect('dashboard')

@login_required
def update_outreach(request):
    instance = get_object_or_404(Outreach, user=request.user)
    if request.method == 'POST':
        form = OutreachForm(request.POST, instance=instance)
        if form.is_valid(): form.save(); messages.success(request, 'Outreach data updated.')
    return redirect('dashboard')

@login_required
def update_challenges(request):
    instance = get_object_or_404(Challenges, user=request.user)
    if request.method == 'POST':
        form = ChallengesForm(request.POST, instance=instance)
        if form.is_valid(): form.save(); messages.success(request, 'Challenges updated.')
    return redirect('dashboard')

@login_required
def update_timelines(request):
    instance = get_object_or_404(Timelines, user=request.user)
    if request.method == 'POST':
        form = TimelinesForm(request.POST, instance=instance)
        if form.is_valid(): form.save(); messages.success(request, 'Timelines updated.')
    return redirect('dashboard')

class GenericCreateView(View):
    form_class = None; model_name = ""
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False); instance.user = request.user; instance.save()
            messages.success(request, f'{self.model_name} entry added.')
        else:
            for field, errors in form.errors.items():
                for error in errors: messages.error(request, f"Error in {field}: {error}")
        return redirect('dashboard')

class GenericUpdateView(UpdateView):
    template_name = 'main_app/generic_form.html'; success_url = reverse_lazy('dashboard')
    def get_queryset(self): return self.model.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title(); return context
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry updated.')
        return super().form_valid(form)

class GenericDeleteView(DeleteView):
    template_name = 'main_app/generic_confirm_delete.html'; success_url = reverse_lazy('dashboard')
    def get_queryset(self): return self.model.objects.filter(user=self.request.user)
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry deleted.')
        return super().form_valid(form)

# -----------------------------------------------------------------------------
# PDF REPORT GENERATION (Updated and Complete)
# -----------------------------------------------------------------------------
@login_required
def download_report_view(request, user_id):
    if not request.user.is_superuser and request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to access this report.")

    target_user = get_object_or_404(User, pk=user_id)
    pdf = PDF('L', 'mm', 'A4') # Landscape orientation
    pdf.add_page()
    
    # Basic Info
    basic_info = getattr(target_user, 'basic_info', None)
    if basic_info:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 7, f"Report for: {target_user.get_full_name() or target_user.username}", 0, 1, 'C')
        pdf.set_font('Arial', '', 9)
        info_text = (f"University: {basic_info.university_name} | PVC: {basic_info.pvc_name} | "
                     f"Date: {basic_info.report_date.strftime('%Y-%m-%d')} | Year: {basic_info.academic_year}")
        pdf.cell(0, 7, info_text, 0, 1, 'C')
        pdf.ln(10)

    # Industry Data
    pdf.chapter_title('Industry Engagement & MoUs')
    industry_data = target_user.industry_entries.all()
    if industry_data:
        headers = ['Industry', 'Sector', 'MoU', 'Engagement', 'Contact', 'Location', 'Programme']
        rows = [[i.industry_name, i.sector_name, i.mou_signed, i.type_of_engagement, i.contact_person, i.location, i.aedp_programme] for i in industry_data]
        col_widths = [40, 30, 15, 50, 45, 35, 40]
        pdf.table(headers, rows, col_widths)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()

    # SSC Data
    pdf.chapter_title('Sector Skill Council (SSC) Engagement & MoU')
    ssc_data = target_user.ssc_entries.all()
    if ssc_data:
        headers = ['SSC Name', 'Sector', 'MoU', 'Programme', 'Engagement', 'Contact']
        rows = [[s.ssc_name, s.sector_name, s.mou_signed, s.aedp_programme, s.type_of_engagement, s.contact_person] for s in ssc_data]
        col_widths = [45, 40, 15, 45, 60, 50]
        pdf.table(headers, rows, col_widths)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()

    # BOAT Data
    pdf.chapter_title('BOAT Collaboration')
    boat_data = target_user.boat_entries.all()
    if boat_data:
        headers = ['Campus/College', 'MoU Signed', 'AEDP Programme', 'Other Information']
        rows = [[b.campus_college_name, b.mou_signed, b.aedp_programme, b.other_information] for b in boat_data]
        col_widths = [70, 30, 70, 85]
        pdf.table(headers, rows, col_widths)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()

    # Program Data
    pdf.chapter_title('Implementation Progress of Selected AEDP Program')
    program_data = target_user.program_entries.all()
    if program_data:
        headers = ['Program Name', 'Component', 'Status', 'Timeline', 'Remarks']
        rows = [[p.program_name, p.component, p.status, p.timeline, p.remarks] for p in program_data]
        col_widths = [60, 50, 30, 45, 70]
        pdf.table(headers, rows, col_widths)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()

    # Campus Data
    pdf.chapter_title('AEDP Program Readiness: Campus & College Details')
    campus_data = target_user.campus_entries.all()
    if campus_data:
        headers = ['Campus', 'Programme', 'Curriculum', 'Continued', 'Converted', 'Faculty', 'Duration', 'Intake']
        rows = [[c.campus_college_name, c.aedp_programme, c.curriculum_type, c.same_aedp_continued, c.existing_degree_converted, c.faculty_department, c.duration, c.student_intake] for c in campus_data]
        col_widths = [40, 40, 50, 20, 20, 40, 25, 20]
        pdf.table(headers, rows, col_widths)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()
    
    pdf.add_page() # New page for non-tabular data

    # Outreach Data
    pdf.chapter_title('Outreach & Stakeholder Engagement')
    outreach_data = getattr(target_user, 'outreach', None)
    if outreach_data:
        data_dict = {
            "Nodal Officer Orientation Conducted": outreach_data.nodal_officer_orientation,
            "No. of Workshops for faculty": outreach_data.faculty_workshops,
            "No. of Workshops for industry/SSCs": outreach_data.industry_workshops,
            "District wise Outreach Program conducted": outreach_data.district_outreach_programs,
            "Parents and other Stakeholder Orientation": outreach_data.parent_orientation,
            "Total Autonomous Colleges on boarded": outreach_data.autonomous_colleges_onboarded,
        }
        pdf.key_value_section(data_dict)
    else:
        pdf.cell(0, 10, 'No data available.'); pdf.ln()

    # Challenges Data
    pdf.chapter_title('Challenges & Risk Mitigation Strategy')
    challenges_data = getattr(target_user, 'challenges', None)
    if challenges_data and challenges_data.content:
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(0, 5, challenges_data.content)
        pdf.ln()
    else:
        pdf.cell(0, 10, 'No challenges specified.'); pdf.ln()

    # Timelines Data
    pdf.chapter_title('Timelines')
    timelines_data = getattr(target_user, 'timelines', None)
    if timelines_data:
        data_dict = {
            "Finalize curriculum": timelines_data.curriculum_finalization,
            "Execution of MoUs": timelines_data.mou_execution,
            "Internal approvals": timelines_data.internal_approvals,
            "Faculty Orientation": timelines_data.faculty_orientation,
            "Launch of Admission Campaign": timelines_data.admission_campaign_launch,
            "Begin Student Enrollment": timelines_data.student_enrollment_begin,
            "Program Commencement": timelines_data.program_commencement,
            "Monthly Progress Reporting": timelines_data.monthly_progress_reporting,
        }
        pdf.key_value_section(data_dict)
    else:
        pdf.cell(0, 10, 'No timeline data available.'); pdf.ln()

    # Generate and return the PDF
    pdf_output = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdf_output, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AEDP_Report_{target_user.username}.pdf"'
    return response
