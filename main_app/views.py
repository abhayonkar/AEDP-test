from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Sum, Avg
import json

# You need to install WeasyPrint: pip install WeasyPrint
from weasyprint import HTML

# -----------------------------------------------------------------------------
# AUTHENTICATION VIEWS
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

# -----------------------------------------------------------------------------
# DASHBOARD VIEW
# -----------------------------------------------------------------------------
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
        # Get or create single-entry instances
        basic_info, _ = BasicInfo.objects.get_or_create(user=request.user)
        outreach, _ = Outreach.objects.get_or_create(user=request.user)
        challenges, _ = Challenges.objects.get_or_create(user=request.user)
        timelines, _ = Timelines.objects.get_or_create(user=request.user)

        # Totals for display
        total_student_commitment = Industry.objects.filter(user=request.user).aggregate(Sum('student_commitment'))['student_commitment__sum'] or 0
        total_boat_students = BOAT.objects.filter(user=request.user).aggregate(Sum('no_of_students'))['no_of_students__sum'] or 0
        total_enrolled_students = Campus.objects.filter(user=request.user).aggregate(Sum('student_enrolled'))['student_enrolled__sum'] or 0

        context = {
            # Forms for single-entry models
            'basic_info_form': BasicInfoForm(instance=basic_info),
            'outreach_form': OutreachForm(instance=outreach),
            'challenges_form': ChallengesForm(instance=challenges),
            'timelines_form': TimelinesForm(instance=timelines),

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

# -----------------------------------------------------------------------------
# ANALYSIS VIEW
# -----------------------------------------------------------------------------
@login_required
def analysis_view(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")

    target_user = get_object_or_404(User, pk=user_id)
    campus_data = Campus.objects.filter(user=target_user)
    boat_data = BOAT.objects.filter(user=target_user)

    # Chart 1 & 2: Enrollment data
    enrollment_labels = [entry.aedp_programme for entry in campus_data]
    enrollment_data = [entry.student_enrolled for entry in campus_data]

    # Chart 3: Stipend data (simple average for demonstration)
    stipend_labels = [entry.aedp_programme for entry in boat_data]
    # A simple way to get a numeric value from a string like "5000-8000"
    stipend_values = []
    for entry in boat_data:
        try:
            # Try to average the range, e.g., "5000-8000" -> 6500
            parts = [int(p.strip()) for p in entry.stipend.split('-')]
            stipend_values.append(sum(parts) / len(parts))
        except (ValueError, AttributeError):
            # If it's not a range or not a number, default to 0
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
# SINGLE-ENTRY FORM HANDLING VIEWS
# -----------------------------------------------------------------------------
@login_required
def update_basic_info(request):
    instance = get_object_or_404(BasicInfo, user=request.user)
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Basic Information updated successfully.')
    return redirect('dashboard')

@login_required
def update_outreach(request):
    instance = get_object_or_404(Outreach, user=request.user)
    if request.method == 'POST':
        form = OutreachForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Outreach data updated successfully.')
    return redirect('dashboard')

@login_required
def update_challenges(request):
    instance = get_object_or_404(Challenges, user=request.user)
    if request.method == 'POST':
        form = ChallengesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Challenges updated successfully.')
    return redirect('dashboard')

@login_required
def update_timelines(request):
    instance = get_object_or_404(Timelines, user=request.user)
    if request.method == 'POST':
        form = TimelinesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timelines updated successfully.')
    return redirect('dashboard')

# -----------------------------------------------------------------------------
# GENERIC VIEWS FOR MULTI-ENTRY MODELS (CREATE, UPDATE, DELETE)
# -----------------------------------------------------------------------------
class GenericCreateView(CreateView):
    """A generic view to handle creation of multi-entry model instances."""
    template_name = 'main_app/generic_form.html'
    success_url = reverse_lazy('dashboard')
    model_name = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry added successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name.title()
        return context

class GenericUpdateView(UpdateView):
    """A generic view to handle updating multi-entry model instances."""
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

class GenericDeleteView(DeleteView):
    """A generic view to handle deleting multi-entry model instances."""
    template_name = 'main_app/generic_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name.title()} entry deleted successfully.')
        return super().form_valid(form)

# -----------------------------------------------------------------------------
# PDF REPORT GENERATION
# -----------------------------------------------------------------------------
@login_required
def download_report_view(request, user_id):
    """
    Generates and serves a PDF report for a given user.
    Admins can download any user's report.
    Regular users can only download their own report.
    """
    if not request.user.is_superuser and request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to access this report.")

    target_user = get_object_or_404(User, pk=user_id)

    # Gather all data for the target user
    industry_data = Industry.objects.filter(user=target_user)
    boat_data = BOAT.objects.filter(user=target_user)
    campus_data = Campus.objects.filter(user=target_user)

    # Totals
    total_student_commitment = industry_data.aggregate(Sum('student_commitment'))['student_commitment__sum'] or 0
    total_boat_students = boat_data.aggregate(Sum('no_of_students'))['no_of_students__sum'] or 0
    total_enrolled_students = campus_data.aggregate(Sum('student_enrolled'))['student_enrolled__sum'] or 0

    # Chart data
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