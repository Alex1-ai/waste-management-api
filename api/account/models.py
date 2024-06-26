
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User should have a username")
        if email is None:
            raise TypeError('Users should have an Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    is_verified=models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects = UserManager()

    def __str__(self):
        return self.email


    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }





# # Create your models here.
# class CustomUser(AbstractUser):
#     name= models.CharField(max_length=70, default='Anonymous')
#     email = models.EmailField(max_length=255, unique=True)


#     username = None

#     USERNAME_FIELD= 'email'
#     REQUIRED_FIELDS= []

#     contact =models.CharField(max_length=20, blank=True, null=True)
#     department =models.CharField(max_length=70, blank=True, null=True)
#     profile_img = models.ImageField(upload_to='profilePics/', blank=True, null=True)
#     gender =models.CharField(max_length=10, blank=True, null=True)


#     session_token = models.CharField(max_length=10, default=0)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)