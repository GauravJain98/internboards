from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from uuid import uuid4
from random import randint

def random_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
##
class Skill(models.Model):
    name = models.CharField(
        max_length = 30,
        unique = True,
        null=False
    )
##
class Custom_User(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    #make it detailed
    address = models.TextField()

#Intern
##
class Intern(models.Model):
    user = models.OneToOneField (
        Custom_User,
        on_delete=models.CASCADE,
    )
    skills = models.ManyToManyField(Skill)
    college = models.CharField(max_length=20,blank=True,null=True, default="")
    location = models.CharField(max_length = 50,default = "New Delhi")
    hired = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        self.user.email = self.email
        self.user.save()
        super().save(*args, **kwargs)
##
class Github(models.Model):
    intern = models.OneToOneField (
        Intern,
        on_delete=models.CASCADE,
    )
    commits = models.IntegerField(null = False,blank=False)
    stars = models.IntegerField(null = False,blank=False)
    followers = models.IntegerField(null = False,blank=False)
    repositories = models.IntegerField(null = False,blank=False)
    following = models.IntegerField(null = False,blank=False)
    def __str__(self):
        return str(self.linkedin_url)
##
class Degree(models.Model):
    college_name = models.CharField(max_length=60,blank=False)
    start = models.CharField(max_length=10,blank=False)
    end= models.CharField(max_length=10,blank=True)
    performance = models.CharField(max_length=3,blank=False)
    name =models.CharField(max_length= 20,default = 'None')
    type_of_degree =models.CharField(max_length= 20,default = 'None')
    description = models.TextField()
    specialise = models.CharField(max_length = 32,blank = False)
    intern = models.ForeignKey(
        Intern,
        on_delete=models.CASCADE,
    ) 
    def __str__(self):
        return str(self.id)
##
class Job(models.Model):
    position = models.CharField(max_length =60,blank=False)
    organization = models.CharField(max_length =90,blank=False)
    location = models.CharField(max_length =90,blank=False)
    start = models.CharField(max_length=10,blank=False)
    end= models.CharField(max_length=10,blank=True)
    description = models.TextField()
    intern = models.ForeignKey(
        Intern,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return str(self.id)
##
class Project(models.Model):
    name = models.CharField(max_length =60,blank=False)
    start = models.CharField(max_length=10,blank=False)
    end= models.CharField(max_length=10)
    description = models.TextField()
    intern = models.ForeignKey(
        Intern,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return str(self.id)

#MainApp

def random_string():
    rnd = str(uuid4().hex)
    while Company.objects.filter(key = rnd ):
        rnd = str(uuid4().hex)
    return rnd
##       
class Company(models.Model):
    name = models.CharField(max_length=30,blank=False)
    website = models.CharField(max_length=60,blank=False, default="")
    email = models.CharField(max_length=200,blank=False, default="")
    description = models.TextField(blank=False , default="")    
    key = models.CharField(max_length=128 , default = random_string ,unique=True )
    address = models.CharField(max_length = 100,default = "")
    city = models.CharField(max_length = 100,default = "")
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    def __str__(self):
        return self.name
##
class Hiring(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE,
        null = False,
        blank = False,
    )
    college = models.CharField(max_length= 20)
    def __str__(self):
        return str(self.college)
##    
class Company_User(models.Model):
    user = models.ForeignKey(
        Custom_User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = True,
        blank = True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name = 'Company',
    )    
    is_active = models.BooleanField(default = 'False')
    is_HR = models.BooleanField(default = 'True')
    added_user = models.ForeignKey(
        'api.Company_User',
        on_delete=models.SET_DEFAULT,
        default = 1,
    )
    share = models.CharField(max_length=4,blank=False, default="1000")
    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        self.share = random_n(4)
        self.user.email = self.email
        self.user.save()
        super().save(*args, **kwargs)

STRIPEND_TYPE = (
    ('Fixed' , "Fixed"),
    ('Negotiable' , "Negotiable"),
    ('Performance based' , "Performance based"),
    ('Unpaid' , "Unpaid"),
)

STRIPEND_RATE = (
    ('/Month' , "/Month"),
    ('/Week' , "/Week"),
    ('Lump Sum' , "Lump Sum"),
)
##
class Category(models.Model):
    name = models.CharField(max_length = 20,blank=False,unique = True)
    def __str__(self):
        return str(self.name)
##      
class Internship(models.Model):
    applications = models.IntegerField(default=0)
    selected = models.IntegerField(default=0)   
    approved = models.BooleanField(default = 'False')
    denied = models.BooleanField(default = 'False')
    allowed = models.BooleanField(default = 'False')
    #perks
    certificate = models.BooleanField(default = 'False')
    flexible_work_hours = models.BooleanField(default = 'False')
    letter_of_recommendation = models.BooleanField(default = 'False')
    free_snacks = models.BooleanField(default = 'False')
    informal_dress_code = models.BooleanField(default = 'False')
    PPO = models.BooleanField(default = 'False')
    stripend_rate = models.CharField(max_length= 20,default = 'None')
    fixed= models.BooleanField(default = 'False')
    negotiable=models.BooleanField(default = 'False')
    performance_based=models.BooleanField(default = 'False')
    catagory = models.CharField(max_length= 20,default = 'None')
    start = models.DateField(auto_now=False, auto_now_add=False)
    end= models.DateField(auto_now=False, auto_now_add=False)
    responsibilities = models.TextField(blank=False , default="")
    stripend = models.CharField(max_length=6,default = "0")
    location = models.CharField(max_length = 50,default = "New Delhi")
    code = models.CharField(max_length = 4,null=False)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name = 'Company',
        null=True
    )
    company_user = models.ForeignKey(
        Company_User,
        on_delete=models.PROTECT,
        verbose_name = 'Company User',
    )
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        self.code = random_n(4)
        if self.denied and self.approved:
            self.denied =False
            self.approved = False
        super().save(*args, **kwargs)
##
class InternshipAvailable(models.Model):
    internship = models.ForeignKey(
        Internship,
        on_delete = models.CASCADE,
        verbose_name=  'Internship'
    )
    college = models.CharField(max_length= 20)

STATUS_TYPE = (
    ('0','Rejected'),
    ('1','Review Period'),
    ('2','Shortlisted'),
    ('3','Interviewee'),
    ('4','Hired'),
)
##
class Submission(models.Model):
    intern = models.ForeignKey (
        Intern,
        on_delete=models.CASCADE,
    )
    college = models.CharField(max_length= 20, blank= True,null=True)
    internship =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
    )
    status = models.CharField(max_length= 20,default = '1')
    selected = models.BooleanField(default = 'False')
    def __str__(self):
        return str(self.id)
##
class Question(models.Model):
    question = models.CharField(max_length=50,default='',blank=False)
    internship =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
    )
    def __str__(self):
        return str(self.question)
##
class Answer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        verbose_name = 'Submission',
    )
    answer_text = models.TextField(blank=False , default = "")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    ) 
    def __str__(self):
        return self.answer_text

#CustomAdmin
##
class SiteAdmin(models.Model):
    user = models.OneToOneField(
        Custom_User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = False,
        blank = False,
    )
    email = models.CharField(max_length=200,blank=False, default="")
    college = models.CharField(max_length= 20)
    def __str__(self):
        return str(self.email)


class College(models.Model):
    name = models.CharField(max_length=200,blank=False)
    sub = models.CharField(max_length=200,blank=False)
    location = models.CharField(max_length=200,blank=False, default="")