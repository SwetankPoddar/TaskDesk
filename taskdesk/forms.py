from django import forms
from django.contrib.auth.models import User
from models import Category, UserProfile, Task
from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'


class createTaskForm(forms.ModelForm):
    task_name = forms.CharField(max_length=128, help_text="Please enter a name for this task",error_messages={'required': 'Please enter your name'})
    task_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),required=False)
    class Meta:
        model = Task
        fields = ('task_name','task_description','due_date','personal_due_date','priority_level','category')
        widgets = {
            'personal_due_date':DateInput(),
            'due_date':DateInput()
        }
        labels = {
            'personal_due_date': 'Please enter the due date',
        }

    def clean(self):
        data = self.cleaned_data
        personal_due_date = data.get('personal_due_date')
        due_date = data.get('due_date')

        if(personal_due_date > due_date):
            self.add_error('personal_due_date','Personal due date should be before the due date of task.')

        todays_date = datetime.today().date()
        if((personal_due_date - todays_date).days <= 0 or (due_date - todays_date).days <= 0):
            self.add_error('due_date','Both the due dates should be in future.')


    def __init__(self, request, *args, **kwargs):
        super(createTaskForm, self).__init__(*args, **kwargs)
        if request.user:
            try:
                queryset = Category.objects.filter(user = request.user)
            except DoesNotExist:
                queryset = Category.objects.none()

        self.fields['category'].queryset = queryset

class createCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','category_description','category_image')
