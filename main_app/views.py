# abhayonkar/aedp-test/AEDP-test-0557ce3e060e3a4334b3e58f088fa172e03244e4/main_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import os
from django.conf import settings
from django.urls import reverse # Import reverse
from .forms import (
    LoginForm, BasicInfoForm, IndustryForm, SSCForm, BOATForm,
    ProgramForm, CampusForm, OutreachForm, ChallengesForm, TimelinesForm
)
from .models import (
    BasicInfo, Industry, SSC, BOAT, Program, Campus, Outreach, Challenges, Timelines
)


# Authentication Views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'main_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Dashboard Views
@login_required
def user_dashboard(request):
    user = request.user
    context = {
        'basic_info_form': BasicInfoForm(instance=BasicInfo.objects.filter(user=user).first()),
        'industry_form': IndustryForm(instance=Industry.objects.filter(user=user).first()),
        'ssc_form': SSCForm(instance=SSC.objects.filter(user=user).first()),
        'boat_form': BOATForm(instance=BOAT.objects.filter(user=user).first()),
        'program_form': ProgramForm(instance=Program.objects.filter(user=user).first()),
        'campus_form': CampusForm(instance=Campus.objects.filter(user=user).first()),
        'outreach_form': OutreachForm(instance=Outreach.objects.filter(user=user).first()),
        'challenges_form': ChallengesForm(instance=Challenges.objects.filter(user=user).first()),
        'timelines_form': TimelinesForm(instance=Timelines.objects.filter(user=user).first()),
    }
    return render(request, 'main_app/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_dashboard')
    
    users_with_data = User.objects.filter(is_staff=False).annotate(
        has_basic_info=models.Exists(BasicInfo.objects.filter(user=models.OuterRef('pk'))),
        has_industry=models.Exists(Industry.objects.filter(user=models.OuterRef('pk'))),
        has_ssc=models.Exists(SSC.objects.filter(user=models.OuterRef('pk'))),
        has_boat=models.Exists(BOAT.objects.filter(user=models.OuterRef('pk'))),
        has_program=models.Exists(Program.objects.filter(user=models.OuterRef('pk'))),
        has_campus=models.Exists(Campus.objects.filter(user=models.OuterRef('pk'))),
        has_outreach=models.Exists(Outreach.objects.filter(user=models.OuterRef('pk'))),
        has_challenges=models.Exists(Challenges.objects.filter(user=models.OuterRef('pk'))),
        has_timelines=models.Exists(Timelines.objects.filter(user=models.OuterRef('pk'))),
    ).order_by('username')
    
    context = {
        'users_with_data': users_with_data
    }
    return render(request, 'main_app/admin_dashboard.html', context)


# Form Handling Views
@login_required
def basic_info_form_view(request):
    instance = BasicInfo.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, instance=instance)
        if form.is_valid():
            basic_info = form.save(commit=False)
            basic_info.user = request.user
            basic_info.save()
            messages.success(request, 'Basic Information saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseBasicInfo') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BasicInfoForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'basic_info_form': form})

@login_required
def industry_form_view(request):
    instance = Industry.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = IndustryForm(request.POST, instance=instance)
        if form.is_valid():
            industry = form.save(commit=False)
            industry.user = request.user
            industry.save()
            messages.success(request, 'Industry Engagement details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseIndustry') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = IndustryForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'industry_form': form})

@login_required
def ssc_form_view(request):
    instance = SSC.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = SSCForm(request.POST, instance=instance)
        if form.is_valid():
            ssc = form.save(commit=False)
            ssc.user = request.user
            ssc.save()
            messages.success(request, 'SSC details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseSSC') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SSCForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'ssc_form': form})

@login_required
def boat_form_view(request):
    instance = BOAT.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = BOATForm(request.POST, instance=instance)
        if form.is_valid():
            boat = form.save(commit=False)
            boat.user = request.user
            boat.save()
            messages.success(request, 'BOAT details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseBOAT') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BOATForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'boat_form': form})


@login_required
def program_form_view(request):
    instance = Program.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            program = form.save(commit=False)
            program.user = request.user
            
            # Calculate the number of curriculum ticks
            count = 0
            if program.major_minor_multidisciplinary_course:
                count += 1
            if program.skill_enhancement_course:
                count += 1
            if program.ability_enhancement_course:
                count += 1
            if program.value_added_course:
                count += 1
            if program.apprenticeship_course:
                count += 1
            program.num_curriculum_ticks = count
            
            program.save()
            messages.success(request, 'Program details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseProgram') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProgramForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'program_form': form})


@login_required
def campus_form_view(request):
    instance = Campus.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = CampusForm(request.POST, instance=instance)
        if form.is_valid():
            campus = form.save(commit=False)
            campus.user = request.user
            campus.save()
            messages.success(request, 'Campus details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseCampus') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CampusForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'campus_form': form})

@login_required
def outreach_form_view(request):
    instance = Outreach.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = OutreachForm(request.POST, instance=instance)
        if form.is_valid():
            outreach = form.save(commit=False)
            outreach.user = request.user
            outreach.save()
            messages.success(request, 'Outreach details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseOutreach') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OutreachForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'outreach_form': form})

@login_required
def challenges_form_view(request):
    instance = Challenges.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ChallengesForm(request.POST, instance=instance)
        if form.is_valid():
            challenges = form.save(commit=False)
            challenges.user = request.user
            challenges.save()
            messages.success(request, 'Challenges details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseChallenges') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChallengesForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'challenges_form': form})

@login_required
def timelines_form_view(request):
    instance = Timelines.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = TimelinesForm(request.POST, instance=instance)
        if form.is_valid():
            timelines = form.save(commit=False)
            timelines.user = request.user
            timelines.save()
            messages.success(request, 'Timelines details saved successfully!')
            return redirect(reverse('user_dashboard') + '#collapseTimelines') # Updated redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TimelinesForm(instance=instance)
    return render(request, 'main_app/user_dashboard.html', {'timelines_form': form})

# Delete Views (using generic confirm delete template)
@login_required
def basic_info_delete(request):
    obj = get_object_or_404(BasicInfo, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Basic Information deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Basic Information'})

@login_required
def industry_delete(request):
    obj = get_object_or_404(Industry, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Industry Engagement details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Industry Engagement'})

@login_required
def ssc_delete(request):
    obj = get_object_or_404(SSC, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'SSC details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'SSC'})

@login_required
def boat_delete(request):
    obj = get_object_or_404(BOAT, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'BOAT details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'BOAT'})

@login_required
def program_delete(request):
    obj = get_object_or_404(Program, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Program details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Program'})

@login_required
def campus_delete(request):
    obj = get_object_or_404(Campus, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Campus details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Campus'})

@login_required
def outreach_delete(request):
    obj = get_object_or_404(Outreach, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Outreach details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Outreach'})

@login_required
def challenges_delete(request):
    obj = get_object_or_404(Challenges, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Challenges details saved successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Challenges'})

@login_required
def timelines_delete(request):
    obj = get_object_or_404(Timelines, user=request.user)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Timelines details deleted successfully.')
        return redirect('user_dashboard')
    return render(request, 'main_app/generic_confirm_delete.html', {'object': obj, 'section_name': 'Timelines'})


# PDF Report Generation
@login_required
def generate_pdf_report(request):
    user = request.user
    basic_info = BasicInfo.objects.filter(user=user).first()
    industry = Industry.objects.filter(user=user).first()
    ssc = SSC.objects.filter(user=user).first()
    boat = BOAT.objects.filter(user=user).first()
    program = Program.objects.filter(user=user).first()
    campus = Campus.objects.filter(user=user).first()
    outreach = Outreach.objects.filter(user=user).first()
    challenges = Challenges.objects.filter(user=user).first()
    timelines = Timelines.objects.filter(user=user).first()

    context = {
        'user': user,
        'basic_info': basic_info,
        'industry': industry,
        'ssc': ssc,
        'boat': boat,
        'program': program,
        'campus': campus,
        'outreach': outreach,
        'challenges': challenges,
        'timelines': timelines,
    }

    template_path = 'main_app/pdf_report.html'
    template = get_template(template_path)
    html = template.render(context)

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_report.pdf"'
    
    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# Analysis View
@login_required
def analysis_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_dashboard')

    total_users = User.objects.filter(is_staff=False).count()
    
    # Example analytics (you can expand this significantly)
    total_basic_info = BasicInfo.objects.count()
    total_industry_mous_signed = Industry.objects.filter(mou_signed='Yes').count()
    total_program_students = Program.objects.aggregate(total_students=models.Sum('student_intake'))['total_students'] # Assuming program had student intake
    
    # Count of each program type
    program_counts = Program.objects.values('program_name').annotate(count=models.Count('program_name')).order_by('program_name')

    context = {
        'total_users': total_users,
        'total_basic_info': total_basic_info,
        'total_industry_mous_signed': total_industry_mous_signed,
        'total_program_students': total_program_students if total_program_students else 0,
        'program_counts': program_counts,
    }
    return render(request, 'main_app/analysis.html', context)