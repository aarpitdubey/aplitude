from django.urls import path,include
from django.contrib import admin
from assessment import views
from django.contrib.auth.views import LogoutView,LoginView


urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('candidate/',include('candidate.urls')),

    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='assessment/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='assessment/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('candidate-detail-page', views.admin_candidate_view,name='candidate-detail-page'),
    path('admin-view-candidate', views.admin_view_candidate_view,name='admin-view-candidate'),
    path('admin-view-candidate-marks', views.admin_view_candidate_marks_view,name='admin-view-candidate-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-candidate/<int:pk>', views.update_candidate_view,name='update-candidate'),
    path('delete-candidate/<int:pk>', views.delete_candidate_view,name='delete-candidate'),

    path('create-assessment-page', views.admin_assessment_view,name='create-assessment-page'),
    path('admin-add-assessment', views.admin_add_assessment_view,name='admin-add-assessment'),
    path('admin-view-assessment', views.admin_view_assessment_view,name='admin-view-assessment'),
    path('delete-assessment/<int:pk>', views.delete_assessment_view,name='delete-assessment'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),


]
