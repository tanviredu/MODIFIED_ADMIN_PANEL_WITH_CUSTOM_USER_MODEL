
''' You Must execute this code before any kind of migration happen '''


from django.db import models

## 1) BaseUserManager will be used to change basic user functionality
## 2) Abstract Base User will create The Base structure
## 3) Persmission mixin will work with the permission 

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy
from email.policy import default


### this is signal dispacher 
### and reciever
from django.db.models.signals import post_save
from django.dispatch import receiver


### make a Custom User manager for managing the user
### we will do it by inheriting the base user manager
### we will inherit the mode
class MyUserManager(BaseUserManager):
    ''' Custom User Model that will work with 
    only with the email and password
    not the username '''

    ### we override the basic user creation 
    ### and the super user creation 

    def _create_user(self,email,password,**extra_fields):
        ## raise some errors
        if not email:
            raise ValueError("Email Must be set!")
        email = self.normalize_email(email) ### this will sanitize the email
        user  = self.model(email = email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user 

    def create_superuser(self,email,password,**extra_fields):
        ''' Super user is just like the other user with some other 
        field is set '''
        
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        
        ## raise some error
        if extra_fields.get('is_staff') is not True:
            raise ValueError("SuperUser Must have is_staff = True ")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super user must have is_superuser = True")

        return self._create_user(email,password,**extra_fields)



## now make the user model base on the Myusermanager
## remember the MyUsermanager is a set of rules that define how it will works
## its not the model
## but you need toassign them them the objects
## so it will adopt the method only
## like user.somting()
## the user will be created with the AbstractbaseUser
## and permission mixin


## this will be the System User Model

class User(AbstractBaseUser,PermissionsMixin):
    ''' The User will have only the email and password '''
    ''' Staff will be deactivated and active will be true '''
    ''' Custom User model will be used to control this '''
    ''' Email will be considered as a email '''

    email     = models.EmailField(unique=True)
    is_staff  = models.BooleanField(ugettext_lazy('Staff Status'),default=False,help_text="Designate weather the user can login in the Admin Panel")
    is_active = models.BooleanField(ugettext_lazy('active'),default=True,help_text="Designates if the user is active")
    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email



## now make a normal Profile Database which have  
##  a one to one relationship witht he user model
## and user part will be filed autometically
## with signal when the user is created 
## its like an event listener will listen the user creation 
## take its object and autometically add it to the profile
## we can do it in the views.py bit we will do it in models.py this time
## and we do the validation here too

class Profile(models.Model):
    user        = models.OneToOneField(User,on_delete = models.CASCADE,related_name="profile")
    username    = models.CharField(max_length = 264,blank=True)
    full_name   = models.CharField(max_length = 264,blank=True)
    address     = models.TextField(max_length = 264,blank=True)
    city        = models.CharField(max_length = 264,blank=True)
    zipcode     = models.CharField(max_length = 264,blank=True)
    country     = models.CharField(max_length = 264,blank=True)
    phone       = models.CharField(max_length = 264,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.user)
    
    def is_fully_field(self):
        
        ## get the fields name
        fields_name = [item.name for item in self.__meta__.get_fields()]

        for field_name in fields_name:
            value = getattr(self,fields_name)
            if value is None or value == "":
                return False 
        return True 



## we make two reciever
## fromt he User model signal
##

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):

    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):

    ## save the profile object
    instance.profile.save()
