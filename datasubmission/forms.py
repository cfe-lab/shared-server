from django import forms
from django.core.exceptions import ValidationError

from . import models


def validate_submission_token(tkn: str):
    if models.SubmissionTokenBody.retrieve_from_token(tkn) is None:
        raise ValidationError("Invalid submission token")


_datafile_help_text = ("An Excel file or Zip archive of CSV files containing "
                       "data for submission to the SHARED project.\n\n"
                       "Your data will be encrypted in transit "
                       "and stored securely.")


class SubmissionForm(forms.Form):
    datafile = forms.FileField(
        label="Data File",
        help_text=_datafile_help_text,
        required=False,
    )
    submission_token = forms.CharField(
        widget=forms.HiddenInput(),
        validators=(validate_submission_token,),
    )
