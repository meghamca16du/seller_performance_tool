from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Feedbacks_table)
class FeedbackAdmin(ImportExportModelAdmin):
    pass

@admin.register(Feedbacks)
class FeedbackAdmin(ImportExportModelAdmin):
    pass

admin.site.register(FeedbackDetails)

