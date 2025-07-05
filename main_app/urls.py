from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Single-Entry Model Updates
    path('update/basic-info/', views.update_basic_info, name='update_basic_info'),
    path('update/outreach/', views.update_outreach, name='update_outreach'),
    path('update/challenges/', views.update_challenges, name='update_challenges'),
    path('update/timelines/', views.update_timelines, name='update_timelines'),

    # PDF Report
    path('report/download/<int:user_id>/', views.download_report_view, name='download_report'),

    # --- Generic CRUD URLs for Multi-Entry Models ---

    # Industry
    path('industry/new/', views.GenericCreateView.as_view(form_class=views.IndustryForm, model_name="Industry"), name='industry_create'),
    path('industry/<int:pk>/edit/', views.GenericUpdateView.as_view(model=views.Industry, form_class=views.IndustryForm), name='industry_update'),
    path('industry/<int:pk>/delete/', views.GenericDeleteView.as_view(model=views.Industry), name='industry_delete'),

    # SSC
    path('ssc/new/', views.GenericCreateView.as_view(form_class=views.SSCForm, model_name="SSC"), name='ssc_create'),
    path('ssc/<int:pk>/edit/', views.GenericUpdateView.as_view(model=views.SSC, form_class=views.SSCForm), name='ssc_update'),
    path('ssc/<int:pk>/delete/', views.GenericDeleteView.as_view(model=views.SSC), name='ssc_delete'),

    # BOAT
    path('boat/new/', views.GenericCreateView.as_view(form_class=views.BOATForm, model_name="BOAT"), name='boat_create'),
    path('boat/<int:pk>/edit/', views.GenericUpdateView.as_view(model=views.BOAT, form_class=views.BOATForm), name='boat_update'),
    path('boat/<int:pk>/delete/', views.GenericDeleteView.as_view(model=views.BOAT), name='boat_delete'),

    # Program
    path('program/new/', views.GenericCreateView.as_view(form_class=views.ProgramForm, model_name="Program"), name='program_create'),
    path('program/<int:pk>/edit/', views.GenericUpdateView.as_view(model=views.Program, form_class=views.ProgramForm), name='program_update'),
    path('program/<int:pk>/delete/', views.GenericDeleteView.as_view(model=views.Program), name='program_delete'),

    # Campus
    path('campus/new/', views.GenericCreateView.as_view(form_class=views.CampusForm, model_name="Campus"), name='campus_create'),
    path('campus/<int:pk>/edit/', views.GenericUpdateView.as_view(model=views.Campus, form_class=views.CampusForm), name='campus_update'),
    path('campus/<int:pk>/delete/', views.GenericDeleteView.as_view(model=views.Campus), name='campus_delete'),
]
