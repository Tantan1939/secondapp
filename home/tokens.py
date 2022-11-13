from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class EmailConfirmationGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, dct, timestamp):
        return (
            six.text_type(dct["name"]) + six.text_type(timestamp) +
            six.text_type(dct["description"])
        )


email_token_generator = EmailConfirmationGenerator()
