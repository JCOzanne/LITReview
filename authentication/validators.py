from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir une lettre', code='password_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'


class ContainsUppercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule',
                code='password_no_uppercase'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule.'


class ContainsLowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre minuscule',
                code='password_no_lowercase'
            )

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre minuscule.'


class ContainsSpecialCharacterValidator:
    special_characters = "!@#$%^&*()+-=[]{}|;:,.<>?"

    def validate(self, password, user=None):
        if not any(char in self.special_characters for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*()+-=[]{}|;:,.<>?)',
                code='password_no_special'
            )

    def get_help_text(self):
        return f'Votre mot de passe doit contenir au moins un caractère spécial parmi : {self.special_characters}'