from django.db import models
from django.contrib.auth.hashers import make_password, check_password


#--------------------------------------------------RegisterUsers Model--------------------------------------------------#


class RegisterUsers(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  # store hashed passwords ideally

    class Meta:
        db_table = 'register_users'
        verbose_name = 'Register User'
        verbose_name_plural = 'Register Users'

    def set_password(self, raw_password):
        """Hash and store the password"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Validate password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username






#--------------------------------------------------LoginUsers Model--------------------------------------------------#

class LoginUsers(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords

    class Meta:
        db_table = 'login_users'

    def set_password(self, raw_password):
        """Hash and store the password"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Validate password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
