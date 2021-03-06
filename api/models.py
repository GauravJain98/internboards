from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from uuid import uuid4
import datetime
from dateutil.relativedelta import relativedelta
from random import randint

def random_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class Address(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    apartment = models.CharField(max_length=10,blank=True,null=True)
    street = models.CharField(max_length=30,blank=True,null=True)
    city = models.CharField(max_length=10,blank=True,null=True)
    zip_code = models.CharField(max_length=8,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)

    def delete(self):
        self.archived = True
        super().save

    class Meta:
        ordering = ['-updated_at']

class College(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200,blank=False)
    address = models.OneToOneField(
        Address,
        on_delete = models.PROTECT,
    )

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']


class Sub(models.Model):
    link = models.CharField(max_length= 20, blank= True,null=True)
    college = models.OneToOneField(
        College,
        on_delete=models.CASCADE,
        verbose_name = 'Sub',
        related_name="sub"
    )
##
class Skill(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(
        max_length = 30,
        unique = True,
        null=False
    )
    def __str__(self):
        return self.name

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Custom_User(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    address = models.ForeignKey(
        Address,
        on_delete = models.PROTECT,
        unique = True,
        null=True,
    )

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']

class ForgotPassword(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey (
        Custom_User,
        on_delete=models.PROTECT,
    )
    code = models.CharField(max_length = 64,unique = True,null=True, default= "")
    def delete(self):
        self.archived = True
        super().save()

    def save(self, *args, **kwargs):
        if self.code == "":
            while True:
                self.code = random_string()[0:64]
                if not ForgotPassword.objects.filter(code = self.code).exists():
                    break
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']
#Intern
##
class Intern(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField (
        Custom_User,
        on_delete=models.CASCADE,
    )
    skills = models.ManyToManyField(Skill)
    sub = models.ForeignKey(
        Sub,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    hired = models.BooleanField(default=False)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Github(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intern = models.OneToOneField (
        Intern,
        on_delete=models.CASCADE,
    )
    following = models.IntegerField(null = False,blank=False)
    stars = models.IntegerField(null = False,blank=False)
    followers = models.IntegerField(null = False,blank=False)
    repositories = models.IntegerField(null = False,blank=False)
    handle = models.CharField(max_length=200,null = False,blank=False)
    origanization = models.CharField(max_length=200,null = False,blank=False)
    owned_private_repo = models.CharField(max_length=200,null = False,blank=False)
    origanization_url = models.CharField(max_length=200,null = False,blank=False)
    owned_public_repos = models.IntegerField(default=0,null = False,blank=False)
    collaborators = models.IntegerField(default=0,null = False,blank=False)
    url = models.CharField(max_length=200,null = False,blank=False)


    def __str__(self):
        return str(self.intern)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Degree(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    college_name = models.CharField(max_length=60,blank=False)
    start = models.DateField( default=datetime.date.today)
    end= models.DateField( default=datetime.date.today)
    performance = models.CharField(max_length=3,blank=False)
    name =models.CharField(max_length= 20,default = 'None')
    type_of_degree =models.CharField(max_length= 20,default = 'None')
    description = models.TextField()
    stream = models.CharField(max_length = 32,blank = False)
    specialise = models.CharField(max_length = 32,blank = True,default = "")
    intern = models.ForeignKey(
        Intern,
        on_delete=models.CASCADE,
        related_name="degrees"
    )
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.start < self.end:
            super().save(*args, **kwargs)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Job(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.CharField(max_length =60,blank=False)
    organization = models.CharField(max_length =90,blank=False)
    '''
    organization = models.ForeignKey(
        Organization,
        on_delete= models.CASCADE
    )
    '''
    location = models.CharField(max_length =90,blank=False)
    start = models.DateField(default=datetime.date.today)
    end= models.DateField( default=datetime.date.today)
    description = models.TextField()
    intern = models.ForeignKey(
        Intern,
        on_delete = models.CASCADE,
        related_name="jobs"
    )
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.start < self.end:
            super().save(*args, **kwargs)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Project(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length =60,blank=False)
    start = models.DateField( default=datetime.date.today)
    end= models.DateField( default=datetime.date.today)
    description = models.TextField()
    intern = models.ForeignKey(
        Intern,
        on_delete = models.CASCADE,
        related_name="projects"
    )
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.start < self.end:
            super().save(*args, **kwargs)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
#MainApp
def random_string():
    rnd = str(uuid4().hex)
    while Company.objects.filter(key = rnd ):
        rnd = str(uuid4().hex)
    return rnd

##
class Company(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30,blank=False)
    website = models.CharField(max_length=60,blank=False, default="")
    email = models.CharField(max_length=200,blank=False, default="")
    description = models.TextField(blank=False , default="")
    key = models.CharField(max_length=128 , default = random_string ,unique=True )
    address = models.ManyToManyField(Address)
    city = models.CharField(max_length = 100,default = "")
    hiring = models.ManyToManyField(Sub , related_name='hiring')

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name + '(' + str(self.id) + ')'

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
##
class Company_User(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
        User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = True,
        blank = True,
    )
    share = models.CharField(max_length=4,blank=True, default="")

    class Meta:
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.share == "" and self.is_HR:
            self.share = random_n(4)
            self.user.save()
        super().save(*args, **kwargs)

    def delete(self):
        self.archived = True
        super().save()

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
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length = 20,blank=False,unique = True)
    def __str__(self):
        return str(self.name)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']

##
STATUS_INTERN_TYPE = (
    ('0','Closed'),
    ('1','Active'),
    ('2','Follow up'),
)


class Internship(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    selected = models.IntegerField(default=0)
    approved = models.BooleanField(default = 'False')
    denied = models.BooleanField(default = 'False')
    allowed = models.BooleanField(default = 'False')
    in_main = models.BooleanField(default = 'False')
    #perks
    status = models.IntegerField(default = 1)
    certificate = models.BooleanField(default = 'False')
    flexible_work_hours = models.BooleanField(default = 'False')
    letter_of_recommendation = models.BooleanField(default = 'False')
    free_snacks = models.BooleanField(default = 'False')
    informal_dress_code = models.BooleanField(default = 'False')
    PPO = models.BooleanField(default = 'False')
    stipend_rate = models.CharField(max_length= 20,default = 'None')
    fixed= models.BooleanField(default = 'False')
    negotiable=models.BooleanField(default = 'False')
    performance_based=models.BooleanField(default = 'False')
    category =models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name = 'Category',
        null=True
    )
    deadline = models.DateField(auto_now=False, auto_now_add=False)
    start = models.DateField(auto_now=False, auto_now_add=False)
    visibility = models.DateField(auto_now=False, auto_now_add=False)
    duration= models.IntegerField(default=0,null=True,blank=True)
    responsibilities = models.TextField(blank=False , default="")
    stipend = models.CharField(max_length=6,default = "0")
    location = models.CharField(max_length = 50,default = "New Delhi")
    code = models.CharField(max_length = 4,null=False,blank=True,default = "")
    id_code = models.CharField(max_length=20,null=False,blank=True)
    available = models.ManyToManyField(Sub , related_name='internships',null=True,blank=True)
    locations = models.ManyToManyField(Address)
    skills = models.ManyToManyField(Skill)
    # company = models.ForeignKey(
    #     Company,
    #     on_delete=models.CASCADE,
    #     verbose_name = 'Company',
    #     null=True
    # )
    company_user = models.ForeignKey(
        Company_User,
        on_delete=models.PROTECT,
        verbose_name = 'Company User',
    )
    def save(self, *args, **kwargs):
        if self.code == "":
            self.visibility = self.deadline + relativedelta(days=15)
            self.code = random_n(4)
        super().save(*args, **kwargs)
        self.id_code = str(self.id) + str(self.code)
        super().save()

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.id)

STATUS_TYPE = (
    ('0','Rejected'),
    ('1','Review Period'),
    ('2','Shortlisted'),
    ('3','Interviewee'),
    ('4','Hired'),
)

##
class Submission(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intern = models.ForeignKey (
        Intern,
        on_delete=models.CASCADE,
    )
    sub = models.ForeignKey(
        Sub,
        on_delete=models.CASCADE,
        related_name="submission",
        null=True
    )
    internship =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
        related_name="submission"
    )
    status = models.IntegerField(default = 1)
    selected = models.BooleanField(default = 'False')
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        self.internship.save()
        super().save(*args, **kwargs)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        unique_together = (("internship", "intern"),)
##
class Question(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.CharField(max_length=50,default='',blank=False)
    placeholder = models.CharField(max_length=50,default='',blank=False)
    internship =  models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        verbose_name = 'Internship',
        related_name = 'questions'
    )
    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['-updated_at']

    def delete(self):
        self.archived = True
        super().save()
##
class Answer(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        verbose_name = 'Submission',
        null=True,
        related_name="answer"
    )
    answer_text = models.TextField(blank=False , default = "")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name = 'answer'
    )
    def __str__(self):
        return self.answer_text

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']

#CustomAdmin
##
class SiteAdmin(models.Model):
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        Custom_User,
        on_delete=models.CASCADE,
        verbose_name = 'User',
        null = False,
        blank = False,
    )
    sub = models.ForeignKey(
        Sub,
        on_delete=models.CASCADE,
        related_name="admin",
        null=True
    )
    def __str__(self):
        return str(self.user.id)

    def delete(self):
        self.archived = True
        super().save()

    class Meta:
        ordering = ['-updated_at']
