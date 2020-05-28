from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from .utils import get_read_time
from markdown_deux import markdown

from six import python_2_unicode_compatible
from tinymce.models import HTMLField

# from django.contrib.auth import get_user_model


# from django.core.validators import RegexValidator

# from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

		
	

# USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'
# User=get_user_model()



# class MyUserManager(BaseUserManager):
# 	def create_user(self, username, email, password=None):
# 		if not email:
# 			raise ValueError('Users must have an email address')

# 		user = self.model(username = username,email = self.normalize_email(email))
					
					
				
# 		user.set_password(password)
# 		user.save(using=self._db)
# 		return user
		

# 	def create_superuser(self, username, email, password=None):
# 		user = self.create_user(username, email, password=password)
				
			
# 		user.is_admin = True
# 		user.is_staff = True
# 		user.save(using=self._db)
# 		return user



# class MyUser(AbstractBaseUser):
# 	username = models.CharField(max_length=100,validators = [RegexValidator(regex = USERNAME_REGEX,message='Username must be alphanumeric or contain numbers',code='invalid_username')],unique=True,null=True,blank=True)
# 	email = models.EmailField(max_length=255,unique=True,verbose_name='email address')
# 	is_admin = models.BooleanField(default=False)
# 	is_staff = models.BooleanField(default=False)
    
    
    
    

    
# 	objects = MyUserManager()
    
	

    

# 	def __str__(self):
# 		return self.email

# 	def get_short_name(self):
		
# 		return self.email


# 	def has_perm(self, perm, obj=None):
		
# 		return True

# 	def has_module_perms(self, app_label):
	
# 		return True

choices = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True)
    
    first_name=models.CharField(max_length=50)
    
    last_name=models.CharField(max_length=50)
    email=models.EmailField(null=True,blank=True)
    gender=models.CharField(max_length=10,choices=choices,default="Male")
    profile_picture = models.ImageField(null=True,blank=True)
    
    birth_date = models.DateField(null=True, blank=True)
    profession=models.CharField(max_length=50,null=True,blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)

    def get_absolute_url(self):
        return reverse("product:profile", kwargs={
            'username': self.user.username})

class Follow(models.Model):
   following = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="following")
   follower = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="follower")
   follow_time = models.DateTimeField(auto_now_add=True)
    
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
        
        


    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    instance.author.save()

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    

    def __str__(self):
        return self.title

class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video_url = models.CharField(max_length=200)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20,blank=False,null=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    
    is_approved = models.BooleanField(default=True )

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True,blank=True, null=True)
    read_time =  models.IntegerField(default=0)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category,blank=True, null=True)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)
    content=HTMLField()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("product:post-detail", kwargs={
            'slug': self.slug
        })

   
    def get_markdown(self):
        content = self.overview
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.overview:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username