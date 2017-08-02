import secrets

from django.test import TestCase

from datasubmission import token
from datasubmission import models


class TestSignatureValidation(TestCase):

    def test_roundtrip(self):
        id_code = secrets.token_hex(4)
        tkn = token.new(id_code)
        parsed = token.validate_and_parse_id_code(tkn)
        msg = "ID code doesn't match after round-trip as token"
        self.assertEqual(id_code, parsed, msg)

    def test_unsigned(self):
        id_code = secrets.token_hex(4)
        unsigned_tkn = "{}.{}".format(id_code, None)
        parsed = token.validate_and_parse_id_code(unsigned_tkn)
        msg = "ID code parsed from unsigned token"
        self.assertIsNone(parsed, msg)

    def test_signed_wrong(self):
        id_code = secrets.token_hex(4)
        other_id_code = secrets.token_hex(4)
        right_msg = token._new_msg(id_code)
        wrong_digest = token._message_digest(
            bytes(token._new_msg(other_id_code), 'utf8'))
        wrongsigned_token = "{}.{}".format(right_msg, wrong_digest)

        msg = "Token with invalid signature accepted"
        self.assertIsNone(
            token.validate_and_parse_id_code(wrongsigned_token),
            msg,
        )


class TestTokenSubmissionBody(TestCase):

    def test_retrieval_from_token(self):
        issuee = 'test issuee'
        token_body = models.SubmissionTokenBody.new(issuee)
        token_body.save()
        id_token = token.new(token_body.id_code)
        retrieved_body = models.SubmissionTokenBody.retrieve_from_token(id_token)
        self.assertEqual(token_body, retrieved_body)
