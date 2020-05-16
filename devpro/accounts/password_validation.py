from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError


class MiniAndMaxLengthValidator(MinimumLengthValidator):
    def __init__(self, max_length=20):
        super().__init__()
        self.max_length = max_length

    def validate(self, password, user=None):
        if self.max_length < len(password) or len(password) < self.min_length:
            raise ValidationError(
                "This password must contain at least %(min_length)d characters and maximum %(max_length)d."
                    .format(self.min_length, self.max_length),
                params={'min_length': self.min_length, 'max_length': self.max_length}
            )

    def get_help_text(self):
        return 'This password must contain at least %(min_length)d characters and maximum %(max_length)d.'\
            .format(self.min_length, self.max_length)


class LowerUpperLettersValidator:

    def validate(self, password, user=None):
        rules = [
            lambda pas: any(x.isupper() for x in pas),
            lambda pas: any(x.islower() for x in pas),
        ]
        if not all(rule(password) for rule in rules):
            raise ValidationError(
                "This password must contain at least one lower letter and one capital letter."
            )

    def get_help_text(self):
        return 'This password must contain at least one lower letter and one capital letter.'
