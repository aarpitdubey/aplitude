from django.db import models
from django.contrib.auth.models import User
# from adminsortable.models import Sortable
# from django.template.defaultfilters import slugify

class Candidate(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Candidate/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


# class Project(Sortable):
#     name = models.CharField("Name", max_length=255)
#     slug = models.SlugField(max_length=255, editable=False)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Project, self).save(*args, **kwargs)