from django.contrib import admin

from . import models

admin.site.register(models.Submission)


class SubmissionTokenBodyAdmin(admin.ModelAdmin):
    readonly_fields = ('token', 'id_code', 'issued_at')
    fields = ('token', 'used', 'issued_to', 'issued_at', 'id_code')


admin.site.register(models.SubmissionTokenBody, SubmissionTokenBodyAdmin)
