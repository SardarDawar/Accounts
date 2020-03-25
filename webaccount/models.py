from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
service=(
('BookKeeping','BookKeeping'),
('VAT','VAT')
)


types=(
('pdf','pdf'),
('docs','docs'),('image','image')
)

class Client(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username


class sector(models.Model):
    company_name    =   models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.company_name
  
class Client_Personal_Info(models.Model):
    Name            =   models.CharField(max_length=300)
    Email           =   models.EmailField(max_length=300)
    Phone_Number    =   models.CharField(max_length=300)

    def __str__(self):
        return self.Name
    

class Client_Company_Info(models.Model):
    client          =   models.ForeignKey(Client_Personal_Info, on_delete=models.CASCADE)
    company_name    =   models.CharField(max_length=300)
    CR              =   models.CharField(max_length=300)
    location        =   models.CharField(max_length=300)
    contact_number  =   models.CharField(max_length=300)
    sector          =   models.ForeignKey(sector, on_delete=models.CASCADE)
    Number_of_branches =   models.IntegerField()
    Number_of_employees =   models.IntegerField()
    Services        =   models.CharField(max_length=300,choices=service) 
    QR_code         =   models.FileField()
    new             =   models.BooleanField(blank=False,default=True)
    active          =   models.BooleanField(blank=False,default=False)
    pending         =   models.BooleanField(blank=False,default=False)
    completed       =   models.BooleanField(blank=False,default=False)
    disabled        =   models.BooleanField(blank=False,default=False)

    def __str__(self):
        return self.company_name

class Required_Documents(models.Model):
    Name    =   models.CharField(max_length=300 , unique=True)
    file_type =   models.CharField(max_length=300,choices=types, unique=True)

    def __str__(self):
        return self.Name

class Subscription_Information(models.Model):
    Services                    =   models.CharField(max_length=300,choices=service) 
    Number_of_subaccounts       =   models.IntegerField()
    package_price               =   models.IntegerField()
    Required_Documents          =   models.ForeignKey(Required_Documents, on_delete=models.CASCADE)
    Relationship_Manager        =   models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Services