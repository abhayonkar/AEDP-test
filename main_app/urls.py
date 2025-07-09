from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Analysis
    path('analysis/<int:user_id>/', views.analysis_view, name='analysis'),

    # Single-Entry Model Updates
    path('update/basic-info/', views.BasicInfoUpdateView.as_view(), name='update_basic_info'),
    path('update/outreach/', views.OutreachUpdateView.as_view(), name='update_outreach'),
    path('update/challenges/', views.ChallengesUpdateView.as_view(), name='update_challenges'),
    path('update/timelines/', views.TimelinesUpdateView.as_view(), name='update_timelines'),

    # PDF Report
    path('report/download/<int:user_id>/', views.download_report_view, name='download_report'),

    # --- CRUD URLs for Multi-Entry Models (REFACTORED) ---

    # Industry
    path('industry/new/', views.IndustryCreateView.as_view(), name='industry_create'),
    path('industry/<int:pk>/edit/', views.IndustryUpdateView.as_view(), name='industry_update'),
    path('industry/<int:pk>/delete/', views.IndustryDeleteView.as_view(), name='industry_delete'),

    # SSC
    path('ssc/new/', views.SSCCreateView.as_view(), name='ssc_create'),
    path('ssc/<int:pk>/edit/', views.SSCUpdateView.as_view(), name='ssc_update'),
    path('ssc/<int:pk>/delete/', views.SSCDeleteView.as_view(), name='ssc_delete'),

    # BOAT
    path('boat/new/', views.BOATCreateView.as_view(), name='boat_create'),
    path('boat/<int:pk>/edit/', views.BOATUpdateView.as_view(), name='boat_update'),
    path('boat/<int:pk>/delete/', views.BOATDeleteView.as_view(), name='boat_delete'),

    # Program
    path('program/new/', views.ProgramCreateView.as_view(), name='program_create'),
    path('program/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('program/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),

    # Campus
    path('campus/new/', views.CampusCreateView.as_view(), name='campus_create'),
    path('campus/<int:pk>/edit/', views.CampusUpdateView.as_view(), name='campus_update'),
    path('campus/<int:pk>/delete/', views.CampusDeleteView.as_view(), name='campus_delete'),
]
