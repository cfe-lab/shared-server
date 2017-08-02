from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from . import models


def _handle_get(req):
    tkn_str = req.GET.get("tkn")
    if tkn_str is None:
        messages.add_message(
            req,
            messages.WARNING,
            "A submission token is required.",
        )
    tkn = models.SubmissionTokenBody.retrieve_from_token(tkn_str)
    if tkn is None and tkn_str is not None:
        messages.add_message(
            req,
            messages.WARNING,
            "Invalid submission token.",
        )
    context = {'messages': messages.get_messages(req)}
    if tkn is not None:
        context['token'] = tkn
    return render(req, 'datasubmission/index.html', context)


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
