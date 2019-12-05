from django.contrib import admin
from articles.models import ArticleModel
from martor.widgets import AdminMartorWidget
from django.db import models
# Register your models here.



@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    empty_value_display = '-empty-'
