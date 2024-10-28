from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Za-z]", password):
            raise ValidationError("Password must contain at least one letter.")
        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit.")

    def get_help_text(self):
        return "Your password must be at least 8 characters long, contain at least one letter and one number."