from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from . import models
from . import forms


def _handle_get_used(req, context, tkn_body):
    return HttpResponse("that one's been used")


def _handle_get_unused(req, context, tkn_body):
    if tkn_body is not None:
        context.update(
            token_body=tkn_body,
            fileform=forms.SubmissionForm({
                'submission_token': tkn_body.token,
            }),
        )
    return render(req, 'datasubmission/index.html', context)


def _handle_get(req):
    tkn_str = req.GET.get("tkn")
    if tkn_str is None:
        messages.add_message(
            req,
            messages.WARNING,
            "A submission token is required.",
        )
    tkn_body = models.SubmissionTokenBody.retrieve_from_token(tkn_str)
    if tkn_body is None and tkn_str is not None:
        messages.add_message(
            req,
            messages.WARNING,
            "Invalid submission token.",
        )
    context = {'messages': messages.get_messages(req)}
    if tkn_body is not None:
        if not tkn_body.used:
            return _handle_get_unused(req, context, tkn_body)
        else:
            return _handle_get_used(req, context, tkn_body)
    else:
        return HttpResponse("not sure what ur up 2 m8")


def _handle_post(req):
    return HttpResponse("Hello, datasubmission (POST)")


@require_http_methods(["GET", "POST"])
def index(req):
    if req.method == "GET":
        return _handle_get(req)
    elif req.method == "POST":
        return _handle_post(req)
    else:
        return HttpResponseNotAllowed()
