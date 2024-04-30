from django import forms
from .models import Projects, Tasks, Users

class UserForm(forms.ModelForm):
    class Meta:
        model = Users  # Specify the model class
        fields = ['Username', 'Email', 'Password', 'Manager']  # Specify the fields from the model you want to include in the form

    Username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'Username'
        })
    )

    Email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'block w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'Email'
        })
    )

    Password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'Password'
        })
    )

    Manager = forms.BooleanField(label='Are you a manager?', required=True)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Projects
        fields = ['Title', 'Description', 'StartDate', 'EndDate', 'Status', 'Priority']

    Title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'Title'
        })
    )

    Description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full ì bg-FormGray h-full my-1 rounded-md',
            'rows': '5',
            'placeholder': 'Description'
        })
    )

    StartDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-FormGray  h-12 rounded-md my-1',
            'placeholder': 'Start Date',
            'type': 'date' 
        })
    )

    EndDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'End Date',
            'type': 'date'
        })
    )

    Status = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-FormGray  h-12 rounded-md my-1',
            'placeholder': 'Status'
        })
    )

    Priority = forms.ChoiceField(
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'Priority'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("StartDate")
        end_date = cleaned_data.get("EndDate")

        if end_date and start_date:
            if end_date < start_date:
                raise forms.ValidationError("End Date must be greater than or equal to Start Date.")

class TaskForm(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = ['Title', 'Description', 'StartDate', 'EndDate']
        
    Title = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'block w-full bg-FormGray h-12 rounded-md my-1',
        'placeholder': 'Title'
    })
    )

    Description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full ì bg-FormGray h-full my-1 rounded-md',
            'rows': '5',
            'placeholder': 'Description'
        })
    )

    StartDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-FormGray  h-12 rounded-md my-1',
            'placeholder': 'Start Date',
            'type': 'date'
        })
    )

    EndDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'w-full bg-FormGray h-12 rounded-md my-1',
            'placeholder': 'End Date',
            'type': 'date'
        })
    )
    
