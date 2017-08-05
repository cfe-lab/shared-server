from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_http_methods

from . import forms
from . import models
from . import store


def after_post_url(tkn_str):
    base = reverse('datasubmission.index')
    return "{}?tkn={}".format(base, tkn_str)


def _handle_get_used(req, context, tkn_body):
    context.update({'token_used': True})
    return render(req, 'datasubmission/index.html', context)


def _handle_get_unused(req, context, tkn_body):
    fileform = forms.SubmissionForm({
        'submission_token': tkn_body.token,
    })
    if tkn_body is not None:
        context.update(fileform=fileform)
    return render(req, 'datasubmission/index.html', context)


def _handle_get(req, context, tkn_str, tkn_body):
    tkn_body = models.SubmissionTokenBody.retrieve_from_token(tkn_str)
    if tkn_body is not None:
        if not tkn_body.used:
            return _handle_get_unused(req, context, tkn_body)
        else:
            return _handle_get_used(req, context, tkn_body)
    else:
        return render(req, 'datasubmission/index.html', context)


def _handle_post(req, context, tkn_str, tkn_body):
    invalid = HttpResponse("Error; reload and try again")
    if tkn_body is None:
        return invalid
    if tkn_body.used:
        redirect(after_post_url(tkn_str), permanent=False)
    fileform = forms.SubmissionForm(req.POST, req.FILES)
    if not fileform.is_valid():
        return invalid
    datafile = fileform.files.get('datafile')
    new_filename = store.save_file(datafile)
    if new_filename is None:
        return invalid
    tkn_body.filename = new_filename
    tkn_body.used = True
    tkn_body.save()
    return redirect(after_post_url(tkn_str), permanent=False)


@require_http_methods(["GET", "POST"])
def index(req):
    tkn_str = req.GET.get("tkn")
    tkn_body = models.SubmissionTokenBody.retrieve_from_token(tkn_str)    
    base_context = {
        'SUPPORT_PERSON': settings.SUPPORT_PERSON,
        'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
        'token_str': tkn_str,
        'token_body': tkn_body,
    }
    if req.method == "GET":
        return _handle_get(req, base_context, tkn_str, tkn_body)
    elif req.method == "POST":
        return _handle_post(req, base_context, tkn_str, tkn_body)
    else:
        return HttpResponseNotAllowed()
