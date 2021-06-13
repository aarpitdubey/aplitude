from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from assessment import models as AMODEL
# from django.shortcuts import render
# from django.template import RequestContext
# from assessment.models import *
# from django.http import Http404

#for showing signup/login button for candidate
def candidateclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'candidate/candidateclick.html')

def candidate_signup_view(request):
    userForm=forms.CandidateUserForm()
    candidateForm=forms.CandidateForm()
    mydict={'userForm':userForm,'candidateForm':candidateForm}
    if request.method=='POST':
        userForm=forms.CandidateUserForm(request.POST)
        candidateForm=forms.CandidateForm(request.POST,request.FILES)
        if userForm.is_valid() and candidateForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            candidate=candidateForm.save(commit=False)
            candidate.user=user
            candidate.save()
            my_candidate_group = Group.objects.get_or_create(name='CANDIDATE')
            my_candidate_group[0].user_set.add(user)
        return HttpResponseRedirect('candidatelogin')
    return render(request,'candidate/candidatesignup.html',context=mydict)

def is_candidate(user):
    return user.groups.filter(name='CANDIDATE').exists()

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def candidate_dashboard_view(request):
    dict={
    
    'total_assessment':AMODEL.Assessment.objects.all().count(),
    'total_question':AMODEL.Question.objects.all().count(),
    }
    return render(request,'candidate/candidate_dashboard.html',context=dict)

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def candidate_exam_view(request):
    assessments=AMODEL.Assessment.objects.all()
    return render(request,'candidate/candidate_exam.html',{'assessments':assessments})

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def take_exam_view(request,pk):
    assessment=AMODEL.Assessment.objects.get(id=pk)
    total_questions=AMODEL.Question.objects.all().filter(assessment=assessment).count()
    questions=AMODEL.Question.objects.all().filter(assessment=assessment)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'candidate/take_exam.html',{'assessment':assessment,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def start_exam_view(request,pk):
    assessment=AMODEL.Assessment.objects.get(id=pk)
    questions=AMODEL.Question.objects.all().filter(assessment=assessment)
    if request.method=='POST':
        pass
    response= render(request,'candidate/start_exam.html',{'assessment':assessment,'questions':questions})
    response.set_cookie('assessment_id',assessment.id)
    return response


@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def calculate_marks_view(request):
    if request.COOKIES.get('assessment_id') is not None:
        assessment_id = request.COOKIES.get('assessment_id')
        assessment=AMODEL.Assessment.objects.get(id=assessment_id)
        
        total_marks=0
        questions=AMODEL.Question.objects.all().filter(assessment=assessment)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        candidate = models.Candidate.objects.get(user_id=request.user.id)
        result = AMODEL.Result()
        result.marks=total_marks
        result.exam=assessment
        result.candidate=candidate
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def view_result_view(request):
    assessments=AMODEL.Assessment.objects.all()
    return render(request,'candidate/view_result.html',{'assessments':assessments})
    

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def check_marks_view(request,pk):
    assessment=AMODEL.Assessment.objects.get(id=pk)
    candidate = models.Candidate.objects.get(user_id=request.user.id)
    results= AMODEL.Result.objects.all().filter(exam=assessment).filter(candidate=candidate)
    return render(request,'candidate/check_marks.html',{'results':results})

@login_required(login_url='candidatelogin')
@user_passes_test(is_candidate)
def candidate_marks_view(request):
    assessments=AMODEL.Assessment.objects.all()
    return render(request,'candidate/candidate_marks.html',{'assessments':assessments})

# def index(data):
#     data = {'project': Project}
#     return render(data, 'candidate/candidatebase.html', context_instance=RequestContext(request))
#
# def project_view(request, project_slug):
#     try:
#         project = Project.objects.get(slug=project_slug)
#     except:
#         raise Http404
#     data = {'project': Project}
#     try:
#         data['prev'] = Project.objects.get(order=Project.order - 1)
#     except:
#         data['prev'] = Project.objects.get(order=Project.objects.count() - 1)
#     try:
#         data['next'] = Project.objects.get(order=Project.order + 1)
#     except:
#         data['next'] = Project.objects.get(order=1)
#
#     return index(data);
