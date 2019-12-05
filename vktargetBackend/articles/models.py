from django.db import models
from markdownx.models import MarkdownxField
from martor.models import MartorField

# Create your models here.
class ArticleModel(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )


    title = models.CharField(max_length=40)
    subtitle = models.CharField(max_length=100)
    short_description = models.CharField(max_length=140)
    body = MartorField()
    author = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now=True)
    tags = models.CharField(max_length=9, choices=YEAR_IN_SCHOOL_CHOICES, default='FR')
    main_theme = models.CharField(max_length=9, choices=YEAR_IN_SCHOOL_CHOICES, default='FR')

    def __str__(self):
        return self.title
