from django import forms
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
from models import Category, UserProfile, Task
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm

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

    def clean(self):
        data = self.cleaned_data
        personal_due_date = data.get('personal_due_date')
        due_date = data.get('due_date')

        todays_date = datetime.today().date()
        if (due_date - todays_date).days <= 0:
            self.add_error('due_date','Due date should be in future.')

        if(personal_due_date):
            if (personal_due_date - todays_date).days <= 0:
                self.add_error('personal_due_date','Personal due date should be in future.')
            if(personal_due_date > due_date):
                self.add_error('personal_due_date','Personal due date should be before the due date of task.')


    def __init__(self, request, *args, **kwargs):
        super(createTaskForm, self).__init__(*args, **kwargs)
        if request.user:
            try:
                queryset = Category.objects.filter(user = request.user)
            except DoesNotExist:
                queryset = Category.objects.none()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['category'].queryset = queryset

class createCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','category_description')

    def __init__(self, *args, **kwargs):
        super(createCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class createSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('high_priority_color','medium_priority_color','low_priority_color')
        widgets = {
            'high_priority_color': TextInput(attrs={'type': 'color'}),
            'medium_priority_color': TextInput(attrs={'type': 'color'}),
            'low_priority_color': TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super(createSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class createUserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name','last_name','email')

    def __init__(self, *args, **kwargs):
        super(createUserSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PasswordChangeCustomForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SetPasswordCustomForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
