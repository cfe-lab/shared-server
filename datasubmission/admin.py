from django.contrib import admin

from . import models


class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'date',
        'token_body',
        'submitted_filename',
        'stored_filename',
    )


admin.site.register(models.Submission, SubmissionAdmin)


class SubmissionTokenBodyAdmin(admin.ModelAdmin):
    readonly_fields = ('token_url', 'id_code', 'issued_at')
    fields = ('token_url', 'used', 'issued_to', 'issued_at', 'id_code')


admin.site.register(models.SubmissionTokenBody, SubmissionTokenBodyAdmin)
