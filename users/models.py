from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



class MyAccountManager(BaseUserManager):
    def create_user(self, f_name, email, phone, password=None):
        if not email:
            raise ValueError('User must have a username')

        user = self.model(
            f_name = f_name,
            email = email,
            phone = phone
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, phone, username ,password, f_name):
        user=self.create_user(
            f_name = f_name,
            username = username,
            password = password,
            phone = phone,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True, null=False)
    phone = models.IntegerField()
    address = models.TextField()
    username = models.TextField(max_length=50, null=False, unique=True)
    password = models.TextField(max_length=50)


    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin  = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_superuser   = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'email']

    objects = MyAccountManager()

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True