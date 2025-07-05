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
# PDF Generation Class using fpdf2
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
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def table(self, headers, data):
        self.set_font('Arial', 'B', 8)
        col_widths = [35] * len(headers) # Adjust column widths as needed
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 7, header, 1, 0, 'C')
        self.ln()

        self.set_font('Arial', '', 8)
        for row in data:
            for i, item in enumerate(row):
                self.multi_cell(col_widths[i], 7, str(item), 1, 'L')
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
# PDF REPORT GENERATION (Updated for fpdf2)
# -----------------------------------------------------------------------------
@login_required
def download_report_view(request, user_id):
    if not request.user.is_superuser and request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to access this report.")

    target_user = get_object_or_404(User, pk=user_id)
    pdf = PDF('L', 'mm', 'A4')
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
        headers = ['Industry', 'Sector', 'MoU', 'Engagement']
        rows = [[i.industry_name, i.sector_name, i.mou_signed, i.type_of_engagement] for i in industry_data]
        pdf.table(headers, rows)
    else:
        pdf.cell(0, 10, 'No data available.')
        pdf.ln()

    # Add other sections in a similar way...
    # (SSC, BOAT, Program, Campus, Outreach, Challenges, Timelines)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdf_output, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AEDP_Report_{target_user.username}.pdf"'
    return response

