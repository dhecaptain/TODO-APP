from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    color = models.CharField(max_length=7,default="#000000")

    def __str__(self) -> str:
        return self.name

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH','High'),
        ('MEDIUM','Medium'),
        ('LOW','Low')
    ]
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]

    title = models.CharField(max_length=200)
    details = RichTextField()
    date = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='MEDIUM')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')
    due_date = models.DateTimeField(null=True,blank=True)

    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    tags = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']
    