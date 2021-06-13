from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from candidate import models as CMODEL
from candidate import forms as CFORM
from django.contrib.auth.models import User



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'assessment/index.html')


def is_candidate(user):
    return user.groups.filter(name='CANDIDATE').exists()

def afterlogin_view(request):
    if is_candidate(request.user):      
        return redirect('candidate/candidate-dashboard')
    else:
        return redirect('create-assessment-page')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_candidate':CMODEL.Candidate.objects.all().count(),
    'total_assessment':models.Assessment.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'assessment/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_candidate_view(request):
    dict={
    'total_candidate':CMODEL.Candidate.objects.all().count(),
    }
    return render(request,'assessment/admin_candidate.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_candidate_view(request):
    candidates= CMODEL.Candidate.objects.all()
    return render(request,'assessment/admin_view_candidate.html',{'candidates':candidates})



@login_required(login_url='adminlogin')
def update_candidate_view(request,pk):
    candidate=CMODEL.Candidate.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=candidate.user_id)
    userForm=CFORM.CandidateUserForm(instance=user)
    candidateForm=CFORM.CandidateForm(request.FILES,instance=candidate)
    mydict={'userForm':userForm,'candidateForm':candidateForm}
    if request.method=='POST':
        userForm=CFORM.CandidateUserForm(request.POST,instance=user)
        candidateForm=CFORM.CandidateForm(request.POST,request.FILES,instance=candidate)
        if userForm.is_valid() and candidateForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            candidateForm.save()
            return redirect('admin-view-candidate')
    return render(request,'assessment/update_candidate.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_candidate_view(request,pk):
    candidate=CMODEL.Candidate.objects.get(id=pk)
    user=User.objects.get(id=candidate.user_id)
    user.delete()
    candidate.delete()
    return HttpResponseRedirect('/admin-view-candidate')


@login_required(login_url='adminlogin')
def admin_assessment_view(request):
    return render(request,'assessment/admin_assessment.html')


@login_required(login_url='adminlogin')
def admin_add_assessment_view(request):
    assessmentForm=forms.AssessmentForm()
    if request.method=='POST':
        assessmentForm=forms.AssessmentForm(request.POST)
        if assessmentForm.is_valid():        
            assessmentForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-assessment')
    return render(request,'assessment/admin_add_assessment.html',{'assessmentForm':assessmentForm})


@login_required(login_url='adminlogin')
def admin_view_assessment_view(request):
    assessments = models.Assessment.objects.all()
    return render(request,'assessment/admin_view_assessment.html',{'assessments':assessments})

@login_required(login_url='adminlogin')
def delete_assessment_view(request,pk):
    assessment=models.Assessment.objects.get(id=pk)
    assessment.delete()
    return HttpResponseRedirect('/admin-view-assessment')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'assessment/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            assessment=models.Assessment.objects.get(id=request.POST.get('assessmentID'))
            question.assessment=assessment
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'assessment/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    assessments= models.Assessment.objects.all()
    return render(request,'assessment/admin_view_question.html',{'assessments':assessments})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(assessment_id=pk)
    return render(request,'assessment/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_candidate_marks_view(request):
    candidates= CMODEL.Candidate.objects.all()
    return render(request,'assessment/admin_view_candidate_marks.html',{'candidates':candidates})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    assessments = models.Assessment.objects.all()
    response =  render(request,'assessment/admin_view_marks.html',{'assessments':assessments})
    response.set_cookie('candidate_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    assessment = models.Assessment.objects.get(id=pk)
    candidate_id = request.COOKIES.get('candidate_id')
    candidate= CMODEL.Candidate.objects.get(id=candidate_id)

    results= models.Result.objects.all().filter(exam=assessment).filter(candidate=candidate)
    return render(request,'assessment/admin_check_marks.html',{'results':results})


def aboutus_view(request):
    return render(request,'assessment/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name  = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'assessment/contactussuccess.html')
    return render(request, 'assessment/contactus.html', {'form':sub})


