from django.urls import include, path
from . import views

app_name = "whistleblower"
urlpatterns = [
    path('', views.home, name='home'),
    path('home-anon/', views.anon_home, name='home_anon'),
    path('home-superadmin/', views.HomeSuperAdmin.as_view(), name='home_superadmin'),
    path('home-admin/', views.home_admin, name='home_admin'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('neighbor-form/', views.neighbor_complaint, name='n-complaint'),
    path('building-form/', views.building_complaint, name='b-complaint'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('view-report/<int:pk>/', views.ReportView.as_view(), name='report_view'),
    path('create-group/', views.create_building_group_page, name='create_group_page'),
    path('create-group/confirm', views.create_building_group, name='create_group'),
    path('join-group/', views.join_building_group_page, name='join_group_page'),
    path('join-group/confirm/', views.join_building_group, name="join_group"),
    path('mark_as_resolved/<int:report_id>/', views.mark_as_resolved, name='mark_as_resolved'),
    path('leave-group/<int:code>/', views.leave_building_group, name='leave_building_group'),
]