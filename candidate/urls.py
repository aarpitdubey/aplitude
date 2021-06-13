from django.urls import path
from candidate import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('candidateclick', views.candidateclick_view),
path('candidatelogin', LoginView.as_view(template_name='candidate/candidatelogin.html'),name='candidatelogin'),
path('candidatesignup', views.candidate_signup_view,name='candidatesignup'),
path('candidate-dashboard', views.candidate_dashboard_view,name='candidate-dashboard'),
path('All-Pending-Test-Page', views.candidate_exam_view,name='All-Pending-Test-Page'),
path('test-page/<int:pk>', views.take_exam_view,name='test-page'),
path('Test-Detail-Page/<int:pk>', views.start_exam_view,name='Test-Detail-Page'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('candidate-marks', views.candidate_marks_view,name='candidate-marks'),
]