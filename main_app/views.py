from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Sum, Avg
import json

# You need to install WeasyPrint: pip install WeasyPrint
from weasyprint import HTML

# -----------------------------------------------------------------------------
# AUTHENTICATION, DASHBOARD, ANALYSIS VIEWS
# -----------------------------------------------------------------------------

def login_view(request):
    """Handles user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main_app/login.html', {'form': form})

def logout_view(request):
    """Handles user logout."""
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    """
    Directs users to the appropriate dashboard (admin or user)
    and populates it with necessary data and forms.
    """
    if request.user.is_superuser:
        # Admin dashboard
        all_users = User.objects.filter(is_superuser=False)
        context = {'all_users': all_users}
        return render(request, 'main_app/admin_dashboard.html', context)
    else:
        # Regular user dashboard
        basic_info, _ = BasicInfo.objects.get_or_create(user=request.user)
        outreach, _ = Outreach.objects.get_or_create(user=request.user)
        challenges, _ = Challenges.objects.get_or_create(user=request.user)
        timelines, _ = Timelines.objects.get_or_create(user=request.user)
        total_student_commitment = Industry.objects.filter(user=request.user).aggregate(Sum('student_commitment'))['student_commitment__sum'] or 0
        total_boat_students = BOAT.objects.filter(user=request.user).aggregate(Sum('no_of_students'))['no_of_students__sum'] or 0
        total_enrolled_students = Campus.objects.filter(user=request.user).aggregate(Sum('student_enrolled'))['student_enrolled__sum'] or 0
        
        context = {
            # Forms for single-entry models
            'basic_info_form': BasicInfoForm(instance=basic_info),
            'outreach_form': OutreachForm(instance=outreach),
            'challenges_form': ChallengesForm(instance=challenges),
            'timelines_form': TimelinesForm(instance=timelines),

            # The actual single-entry objects for display
            'basic_info': basic_info,
            'outreach': outreach,
            'challenges': challenges,
            'timelines': timelines,

            # Forms for adding new multi-entry items
            'industry_form': IndustryForm(),
            'ssc_form': SSCForm(),
            'boat_form': BOATForm(),
            'program_form': ProgramForm(),
            'campus_form': CampusForm(),

            # Existing data for multi-entry models
            'industry_entries': Industry.objects.filter(user=request.user),
            'ssc_entries': SSC.objects.filter(user=request.user),
            'boat_entries': BOAT.objects.filter(user=request.user),
            'program_entries': Program.objects.filter(user=request.user),
            'campus_entries': Campus.objects.filter(user=request.user),
            
            # Totals
            'total_student_commitment': total_student_commitment,
            'total_boat_students': total_boat_students,
            'total_enrolled_students': total_enrolled_students,
        }
        return render(request, 'main_app/user_dashboard.html', context)

@login_required
def analysis_view(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    target_user = get_object_or_404(User, pk=user_id)
    campus_data = Campus.objects.filter(user=target_user)
    boat_data = BOAT.objects.filter(user=target_user)
    enrollment_labels = [entry.aedp_programme for entry in campus_data]
    enrollment_data = [entry.student_enrolled for entry in campus_data]
    stipend_labels = [entry.aedp_programme for entry in boat_data]
    stipend_values = []
    for entry in boat_data:
        try:
            parts = [int(p.strip()) for p in entry.stipend.split('-')]
            stipend_values.append(sum(parts) / len(parts))
        except (ValueError, AttributeError):
            stipend_values.append(0)
    context = {
        'target_user': target_user,
        'enrollment_labels': json.dumps(enrollment_labels),
        'enrollment_data': json.dumps(enrollment_data),
        'stipend_labels': json.dumps(stipend_labels),
        'stipend_data': json.dumps(stipend_values),
    }
    return render(request, 'main_app/analysis.html', context)

# -----------------------------------------------------------------------------
# SINGLE-ENTRY FORM HANDLING VIEWS (REFACTORED)
# -----------------------------------------------------------------------------
class SingleEntryUpdateView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('dashboard')
    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(user=self.request.user)
        return obj
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} updated successfully.')
        return super().form_valid(form)
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.title()}: {error}")
        return redirect('dashboard')

class BasicInfoUpdateView(SingleEntryUpdateView):
    model = BasicInfo
    form_class = BasicInfoForm

class OutreachUpdateView(SingleEntryUpdateView):
    model = Outreach
    form_class = OutreachForm

class ChallengesUpdateView(SingleEntryUpdateView):
    model = Challenges
    form_class = ChallengesForm

class TimelinesUpdateView(SingleEntryUpdateView):
    model = Timelines
    form_class = TimelinesForm

# -----------------------------------------------------------------------------
# GENERIC BASE VIEWS FOR MULTI-ENTRY MODELS
# -----------------------------------------------------------------------------
class GenericCreateView(LoginRequiredMixin, CreateView):
    template_name = 'main_app/generic_form.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry added successfully.')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        return context

class GenericUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'main_app/generic_form.html'
    success_url = reverse_lazy('dashboard')
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        return context
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry updated successfully.')
        return super().form_valid(form)

class GenericDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'main_app/generic_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry deleted successfully.')
        return super().form_valid(form)

# -----------------------------------------------------------------------------
# CONCRETE VIEWS FOR MULTI-ENTRY MODELS (FIX FOR CIRCULAR IMPORT)
# -----------------------------------------------------------------------------

# --- Industry Views ---
class IndustryCreateView(GenericCreateView):
    model = Industry
    form_class = IndustryForm
class IndustryUpdateView(GenericUpdateView):
    model = Industry
    form_class = IndustryForm
class IndustryDeleteView(GenericDeleteView):
    model = Industry

# --- SSC Views ---
class SSCCreateView(GenericCreateView):
    model = SSC
    form_class = SSCForm
class SSCUpdateView(GenericUpdateView):
    model = SSC
    form_class = SSCForm
class SSCDeleteView(GenericDeleteView):
    model = SSC

# --- BOAT Views ---
class BOATCreateView(GenericCreateView):
    model = BOAT
    form_class = BOATForm
class BOATUpdateView(GenericUpdateView):
    model = BOAT
    form_class = BOATForm
class BOATDeleteView(GenericDeleteView):
    model = BOAT

# --- Program Views ---
class ProgramCreateView(GenericCreateView):
    model = Program
    form_class = ProgramForm
class ProgramUpdateView(GenericUpdateView):
    model = Program
    form_class = ProgramForm
class ProgramDeleteView(GenericDeleteView):
    model = Program

# --- Campus Views ---
class CampusCreateView(GenericCreateView):
    model = Campus
    form_class = CampusForm
class CampusUpdateView(GenericUpdateView):
    model = Campus
    form_class = CampusForm
class CampusDeleteView(GenericDeleteView):
    model = Campus

# -----------------------------------------------------------------------------
# PDF REPORT GENERATION
# -----------------------------------------------------------------------------
@login_required
def download_report_view(request, user_id):
    if not request.user.is_superuser and request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to access this report.")
    target_user = get_object_or_404(User, pk=user_id)
    industry_data = Industry.objects.filter(user=target_user)
    boat_data = BOAT.objects.filter(user=target_user)
    campus_data = Campus.objects.filter(user=target_user)
    total_student_commitment = industry_data.aggregate(Sum('student_commitment'))['student_commitment__sum'] or 0
    total_boat_students = boat_data.aggregate(Sum('no_of_students'))['no_of_students__sum'] or 0
    total_enrolled_students = campus_data.aggregate(Sum('student_enrolled'))['student_enrolled__sum'] or 0
    
    labels = [entry.aedp_programme for entry in campus_data]
    data = [entry.student_enrolled for entry in campus_data]
    context = {
        'user_data': target_user,
        'basic_info': getattr(target_user, 'basic_info', None),
        'industry_data': industry_data,
        'ssc_data': SSC.objects.filter(user=target_user),
        'boat_data': boat_data,
        'program_data': Program.objects.filter(user=target_user),
        'campus_data': campus_data,
        'outreach_data': getattr(target_user, 'outreach', None),
        'challenges': getattr(target_user, 'challenges', None),
        'timelines': getattr(target_user, 'timelines', None),
        'total_student_commitment': total_student_commitment,
        'total_boat_students': total_boat_students,
        'total_enrolled_students': total_enrolled_students,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data)
    }
    html_string = render_to_string('main_app/pdf_report.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="AEDP_Report_{target_user.username}.pdf"'
    return response
