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

# You need to install WeasyPrint: pip install WeasyPrint
from io import BytesIO
from xhtml2pdf import pisa
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
        }
        return render(request, 'main_app/user_dashboard.html', context)

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
class GenericCreateView(View):
    """A generic view to handle creation of multi-entry model instances."""
    form_class = None
    model_name = ""

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, f'{self.model_name} entry added successfully.')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
        return redirect('dashboard')

class GenericUpdateView(UpdateView):
    """A generic view to handle updating multi-entry model instances."""
    template_name = 'main_app/generic_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Ensure users can only edit their own objects
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Add the model's verbose name to the context to use in the template
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
        # Ensure users can only delete their own objects
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
    Generates and serves a PDF report for a given user using xhtml2pdf.
    Admins can download any user's report.
    Regular users can only download their own report.
    """
    # Security check
    if not request.user.is_superuser and request.user.id != user_id:
        return HttpResponseForbidden("You do not have permission to access this report.")

    target_user = get_object_or_404(User, pk=user_id)

    # Gather all data for the target user (this part is unchanged)
    context = {
        'user_data': target_user,
        'basic_info': getattr(target_user, 'basic_info', None),
        'industry_data': target_user.industry_entries.all(),
        'ssc_data': target_user.ssc_entries.all(),
        'boat_data': target_user.boat_entries.all(),
        'program_data': target_user.program_entries.all(),
        'campus_data': target_user.campus_entries.all(),
        'outreach_data': getattr(target_user, 'outreach', None),
        'challenges': getattr(target_user, 'challenges', None),
        'timelines': getattr(target_user, 'timelines', None),
    }

    # Render HTML template to a string
    html_string = render_to_string('main_app/pdf_report.html', context)

    # Create a PDF file in memory
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)

    if not pdf.err:
        # If there are no errors, return the PDF as a response
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="AEDP_Report_{target_user.username}.pdf"'
        return response

    # If there was an error, return an error message
    return HttpResponse("Error Rendering PDF", status=400)

