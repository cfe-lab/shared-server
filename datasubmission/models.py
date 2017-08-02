import secrets

from django.db import models
from django.utils import timezone

from . import token


class Submission(models.Model):
    date = models.DateTimeField("date submitted")
    submitter = models.CharField("submitter", max_length=256)
    slug = models.CharField("unique slug", max_length=16)
    # TODO(nknight): content field?

    def __str__(self):
        tmpl = "{} {}"
        return tmpl.format(self.submitter, self.date)


def default_new_id_code():
    return secrets.token_hex(4)

class SubmissionTokenBody(models.Model):
    '''
    '''
    id_code = models.CharField(
        "ID Code",
        unique=True,
        max_length=32,
       default=default_new_id_code
    )
    issued_to = models.CharField("Issued To", max_length=128)
    issued_at = models.DateTimeField("Issued At", default=timezone.now)
    used = models.BooleanField("Used", default=False)

    def __str__(self):
        tmpl = "issued to {} at {} {}"
        used_msg = "(used)" if self.used else ""
        return tmpl.format(self.issued_to, self.issued_at, used_msg)

    @classmethod
    def new(cls, issued_to=None):
        return cls(issued_to=issued_to)

    @property
    def token(self):
        return token.new(self.id_code)

    @classmethod
    def retrieve_from_token(cls, tkn):
        try:
            id_code = token.validate_and_parse_id_code(tkn)
            if id_code is None:
                return None
            token_body = cls.objects.get(id_code__exact=id_code)
            return token_body
        except Exception as e:
            # TODO(nknight): log the exception
            print(e)
            return None
