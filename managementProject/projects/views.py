import datetime
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.conf import settings
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import secrets

from .forms import UserForm, ProjectForm, TaskForm
from .models import Projects, Tasks, Users



def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        form = UserForm()  # Initialize the form
        return render(request, 'register.html', {'form': form})
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            hashed_password = make_password(form.cleaned_data['Password'])
            token = secrets.token_urlsafe(30)        # Token for verification
            user_instance = form.save(commit=False)  # Get the unsaved model instance
            user_instance.Password = hashed_password # Update with hashed password
            user_instance.Token = token
            user_instance.save()              
            activation_link = f"{settings.DOMAIN}/activate/{token}"

            message = Mail(
                from_email=settings.SENDER_EMAIL,
                to_emails=user_instance.Email,
                subject='Sending with Twilio SendGrid is Fun',
                html_content=activation_link)
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                sg.send(message)
            except Exception as e:
                print(e.message)

            return redirect('projects')                                           
        else:     
            print(form.errors)                                                                                      
            return render(request, 'register.html', {'error': "form error"})
        
def activate(request, tokenURL):
    try:
        user = Users.objects.get(Token=tokenURL)
        user.Verified = True
        user.Token = ''
        # Save the changes to the database
        user.save()
        payload = {
        'user_id': user.PKUser,
        'username': user.Username,
        'email': user.Email,
        'manager': user.Manager,
        'verified': user.Verified
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = HttpResponseRedirect(reverse('projects'))
        response.set_cookie('jwt_token', token, expires=timezone.now() + datetime.timedelta(hours=24))
        return response
    except Users.DoesNotExist:
        return HttpResponse("Invalid activation link", status=404)



def projects(request):

    if request.method == 'GET':
        projects = Projects.objects.all()  # Fetch all existing projects
        form = ProjectForm()  # Initialize the form
        return render(request, 'projects.html', {'projects': projects, 'form': form})

    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()                                                                                 #validation, instantiation and insertion is all automatic based on forms.py and models.py
            return redirect('projects')                                                                 #redirect to the same page to display updated projects
        else:                                                                                           #form is not valid, re-render the page with the form and existing projects
            return render(request, 'projects.html', {'error': "form error"})

def project(request, project_id):
    
    project = Projects.objects.get(PKProject=project_id)
    tasks = Tasks.objects.filter(FKProject=project_id)
    htmlTasks = []
    for task in tasks:
        taskData = {
            'id': task.id,
            'name': task.Title,
            'start': task.StartDate.strftime('%Y-%m-%d'),  # Format date as 'YYYY-MM-DD'
            'end': task.EndDate.strftime('%Y-%m-%d'),     
        }
        htmlTasks.append(taskData)
    print(htmlTasks)
        

    if request.method == 'GET':
        form = TaskForm()  
        return render(request, 'project.html', {'project': project, 'tasks': htmlTasks, 'form': form})
    
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # don't commit to database yet
            task.FKProject_id = project_id  # add the foreign key manually
            task.save()
            return redirect('project', project_id)
        else:
            errors = form.errors.as_data()  # Get the form errors
            return render(request, 'project.html', {'project': project, 'tasks': htmlTasks, 'form': form, 'errors': errors})

