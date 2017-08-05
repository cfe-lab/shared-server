from django.contrib import admin

from . import models

admin.site.register(models.Submission)


class SubmissionTokenBodyAdmin(admin.ModelAdmin):
    readonly_fields = ('token_url', 'id_code', 'issued_at', 'filename')
    fields = ('token_url', 'used', 'issued_to', 'issued_at', 'id_code', 'filename')


admin.site.register(models.SubmissionTokenBody, SubmissionTokenBodyAdmin)
