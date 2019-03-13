from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_image = models.ImageField(upload_to='profile-images/',default = 'profile-images/default.png', blank=True)
    high_priority_color = models.CharField(max_length=6,default='FF0000')
    medium_priority_color = models.CharField(max_length=6,default='FFA500')
    low_priority_color = models.CharField(max_length=6,default='00FF00')
    color_mode = models.CharField(max_length=1,default='D')

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name

class Category(models.Model):
    user = models.ForeignKey(User)
    category_name = models.CharField(max_length = 45, blank=False)
    category_description = models.CharField(max_length = 250, blank = True)
    created_at = models.DateTimeField(editable = False)


    def __str__(self):
        return self.category_name

    class Meta:
        unique_together = ('user','category_name')
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Category,self).save(*args,**kwargs)

class Task(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    due_date = models.DateField(blank = False)
    personal_due_date =  models.DateField(default=None, blank=True, null=True)

    task_name = models.CharField(blank = False, max_length = 45)
    task_description = models.CharField(blank = True, max_length = 250)

    created_at = models.DateTimeField(editable = False)
    modifed_at = models.DateTimeField()

    done = models.BooleanField()

    priority_level_choices = (
    (1,'Low'),
    (2,'Medium'),
    (3,'High')
    )

    priority_level = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(1)],blank = False,
    choices=priority_level_choices, default=2)

    def __str__(self):
        return self.task_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.done = False
        self.modifed_at = timezone.now()
        return super(Task,self).save(*args,**kwargs)
