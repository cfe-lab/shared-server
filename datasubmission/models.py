import logging
import secrets

from django.db import models
from django.urls import reverse
from django.utils import timezone

from . import token


logger = logging.getLogger(__name__)


def default_new_id_code():
    return secrets.token_hex(4)


class SubmissionTokenBody(models.Model):
    '''
    '''
    id_code = models.CharField(
        "ID Code",
        unique=True,
        max_length=32,
        default=default_new_id_code,
    )
    issued_to = models.CharField("Issued To", max_length=128)
    issued_at = models.DateTimeField("Issued At", default=timezone.now)

    def __str__(self):
        tmpl = "issued to {} at {}"
        return tmpl.format(self.issued_to, self.issued_at)

    @classmethod
    def new(cls, issued_to=None):
        return cls(issued_to=issued_to)

    @property
    def token(self):
        return token.new(self.id_code)

    @property
    def token_url(self):
        tkn = self.token
        base = reverse('datasubmission.index')
        return "{}?tkn={}".format(base, tkn)

    @classmethod
    def retrieve_from_token(cls, tkn):
        id_code = token.validate_and_parse_id_code(tkn)
        if id_code is None:
            return None
        try:
            token_body = cls.objects.get(id_code__exact=id_code)
            return token_body
        except Exception as e:
            msg = "Exception while retrieving token from ID code: {}"
            logger.info(msg.format(e))
            return None


class Submission(models.Model):
    date = models.DateTimeField("date submitted", default=timezone.now)
    token_body = models.ForeignKey(
        SubmissionTokenBody,
        on_delete=models.CASCADE,
    )
    submitted_filename = models.CharField(max_length=256)
    stored_filename = models.CharField(max_length=256)

    def __str__(self):
        tmpl = "{} {}"
        submitter = self.token_body.issued_to
        return tmpl.format(submitter, self.date)
