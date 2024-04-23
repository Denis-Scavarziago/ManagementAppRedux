from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser         # Django built-in model


# Create your models here.

class Users(AbstractUser):
    PKUser = models.AutoField(primary_key=True)
    # Remove the unique constraint for the username
    username = models.CharField(max_length=150, unique=False)
    # password: hashed password
    # email
    # first_name:
    # last_name:
    # is_staff: A boolean indicating whether the user is a staff member (has access to the admin interface).
    # is_active: A boolean indicating whether the user account is active.
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    # date_joined: The date and time when the user account was created.

    # get_username()
    # get_full_name()
    # get_short_name()
    # set_password(raw_password): Sets the password for the user, hashing it for storage.
    # check_password(raw_password): Checks whether the given raw password matches the hashed password stored for the user.
    # set_unusable_password(): Marks the user's password as unusable (password reset).
    # has_usable_password(): Checks whether the user has a usable password.
    # get_session_auth_hash(): Returns a hash of the user's password, used to validate sessions.
    # email_user(subject, message, from_email=None, **kwargs): Sends an email to the user.

    def __str__(self):
        return self.username


class Projects(models.Model):
    FKUser = models.ForeignKey(Users, on_delete=models.CASCADE)
    PKProject = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=20)  
    Description = models.TextField()
    StartDate = models.DateField(default=timezone.now)  # autoset to current date
    EndDate = models.DateField()                           
    Status = models.CharField(max_length=20, default='Pending')  
    Priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High')
        ])

    def __str__(self):  # value to return when casted to str()
        return self.Title

class Tasks(models.Model):
    FKProject = models.ForeignKey(Projects, on_delete=models.CASCADE)
    Title = models.CharField(max_length=20) 
    Description = models.TextField()
    StartDate = models.DateField()  
    EndDate = models.DateField()     

    def save(self):
        self.FKProject.EndDate = max(self.FKProject.EndDate, self.EndDate)
        super().save()

    def __str__(self):
        return self.Title

class Personnel(models.Model):
    FKProject = models.ForeignKey(Projects, on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    Surname = models.CharField(max_length=20)
    Role = models.CharField(max_length=20)
    Email = models.EmailField()

    def __str__(self):
        return f"{self.Name} {self.Surname}"                                                                                # Concatenate Name and Surname
