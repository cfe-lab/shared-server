'''Views for retrieving the data submission page and handling submitted data'''
import secrets

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from . import forms
from . import models
from . import store


def _handle_get(req, context, tkn_body):
    if tkn_body is not None:
        fileform = forms.SubmissionForm({
            "submission_token": tkn_body.token,
        })
        context.update(fileform=fileform)
    return render(req, "datasubmission/index.html", context)


def _handle_post(req, context, tkn_str, tkn_body):
    invalid = HttpResponse("Error; reload and try again")
    if tkn_body is None:
        return invalid
    fileform = forms.SubmissionForm(req.POST, req.FILES)
    if not fileform.is_valid():
        return invalid
    datafile = fileform.files.get("datafile")
    new_filename = secrets.token_hex(8)
    store.save_file(datafile, new_filename)
    submission = models.Submission(
        token_body=tkn_body,
        submitted_filename=datafile.name,
        stored_filename=new_filename,
    )
    submission.save()
    return redirect("datasubmission.success", permanent=False)


@require_http_methods(["GET", "POST"])
def index(req):
    tkn_str = req.GET.get("tkn")
    tkn_body = models.SubmissionTokenBody.retrieve_from_token(tkn_str)
    base_context = {
        "SUPPORT_PERSON": settings.SUPPORT_PERSON,
        "SUPPORT_EMAIL": settings.SUPPORT_EMAIL,
        "token_str": tkn_str,
        "token_body": tkn_body,
    }
    if req.method == "GET":
        return _handle_get(req, base_context, tkn_body)
    elif req.method == "POST":
        return _handle_post(req, base_context, tkn_str, tkn_body)
    else:
        return HttpResponseNotAllowed()


@require_http_methods(["GET"])
def success(req):
    return render(req, "datasubmission/success.html")
