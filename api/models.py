from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from uuid import uuid4

#Intern

class Social(models.Model):
    linkedin_url = models.CharField(max_length = 200,null = True,blank=True)
    github = models.CharField(max_length = 200,null = True,blank=True)
    def __str__(self):
        return str(self.linkedin_url)

class Intern(models.Model):
    name = models.CharField(max_length=30,blank=True)
    email = models.CharField(max_length=200,blank=False, default="")
    degrees = models.TextField(null = True,blank=True)
    user = models.OneToOneField (
        User,
        on_delete=models.CASCADE,
    )
    social = models.OneToOneField(
        Social,
        on_delete = models.CASCADE,
    )
    skills= models.TextField(null = True,blank=True,default="")
    sub = models.CharField(max_length=20,blank=True,null=True, default="")
    location = models.CharField(max_length = 50,default = "New Delhi")
    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        self.user.email = self.email
        self.user.save()
        super().save(*args, **kwargs)

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

class Hiring(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE,
        null = False,
        blank = False,
    )
    sub = models.CharField(max_length= 20,default = 'None')
    def __str__(self):
        return str(self.sub)
    
class Company_User(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = True,
        blank = True,
    )
    email = models.CharField(max_length=200,blank=False, default="")
    company_id = models.ForeignKey(
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
    name = models.CharField(max_length =100,blank=True)
    share = models.CharField(max_length=4,blank=False, default="1000")
    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        
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

class Catagory(models.Model):
    name = models.CharField(max_length = 20,blank=False,unique = True)
    def __str__(self):
        return str(self.name)
        
class Internship(models.Model):
    interns_applied = models.ManyToManyField(Intern)
    application_number = models.IntegerField(default=0)
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
    responsibility = models.TextField(blank=False , default="")
    stripend = models.CharField(max_length=6,default = "0")
    location = models.CharField(max_length = 50,default = "New Delhi")
 
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
        if self.denied and self.approved:
            self.denied =False
            self.approved = False
        super().save(*args, **kwargs)

class InternshipAvailable(models.Model):
    internship = models.ForeignKey(
        Internship,
        on_delete = models.CASCADE,
        verbose_name=  'Internship'
    )
    sub = models.CharField(max_length= 20,default = 'None')

class InternshipForm(ModelForm):
    class Meta:
        model = Internship
        fields = ['catagory','location','fixed','negotiable','performance_based','stripend','stripend_rate','responsibility','start','end','certificate','flexible_work_hours','letter_of_recommendation','free_snacks','informal_dress_code','PPO']

STATUS_TYPE = (
    ('0','Rejected'),
    ('1','Review Period'),
    ('2','Shortlisted'),
    ('3','Interviewee'),
    ('4','Hired'),
)

class Submission(models.Model):
    intern = models.ForeignKey (
        Intern,
        on_delete=models.CASCADE,
    )
    sub = models.CharField(max_length= 20,default = 'None',blank= True,null=True)
    internship_id =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
    )
    status = models.CharField(max_length= 20,default = '1')
    selected = models.BooleanField(default = 'False')
    def __str__(self):
        return str(self.id)

class Question(models.Model):
    question = models.CharField(max_length=50,default='',blank=False)
    internship_id =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
    )
    def __str__(self):
        return str(self.question)

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

class SiteAdmin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = False,
        blank = False,
    )
    email = models.CharField(max_length=200,blank=False, default="")
    sub = models.CharField(max_length= 20,default = 'iiit')
    def __str__(self):
        return str(self.email)

