from django.db import models
# from adminsortable.models import Sortable
# from django.template.defaultfilters import slugify


from candidate.models import Candidate
class Assessment(models.Model):
   assessment_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.assessment_name

class Question(models.Model):
    assessment=models.ForeignKey(Assessment,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    exam = models.ForeignKey(Assessment,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


# class Project(Sortable):
#     name = models.CharField("Name", max_length=255)
#     slug = models.SlugField(max_length=255, editable=False)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Project, self).save(*args, **kwargs)