from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


admin.site.register(
    [Customer, Post, PostImage, Comment])
