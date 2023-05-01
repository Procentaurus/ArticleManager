from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class MyUserManager(BaseUserManager):

    def create_user(self, email, username,password=None):
        if not email:
            raise ValueError("User must have an email adress.")
        if not username:
            raise ValueError("User must have an username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    # def user_directory_path(instance, filename):
    #     return 'avatars/user_{0}/{1}'.format(instance.id, filename)

    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)
    isEditor = models.BooleanField(default=False, blank=True)
    isProjectManager = models.BooleanField(default=False, blank=True)
    
    #hide_mail = models.BooleanField(default=True)
    #phone_number = models.PositiveIntegerField(null=True, unique=True, validators=[MinValueValidator(111111111), MaxValueValidator(999999999)])
    #image = models.ImageField(null=True, blank=True, upload_to=user_directory_path, default="model.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_staff =models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.username
