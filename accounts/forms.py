from django import forms


class LoginForm(forms.Form):
    
    EMAIL_FIELD_ERROR = "Please enter a valid email"
    PASSWORD_FIELD_ERROR = "You have to enter a password"

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = self.EMAIL_FIELD_ERROR
        self.fields["email"].error_messages["invalid"] = self.EMAIL_FIELD_ERROR
        self.fields["password"].error_messages["required"] = self.PASSWORD_FIELD_ERROR

    email = forms.EmailField(label="")
    email.widget.attrs.update(
        {
            "class": "form-control",
            "id": "id_modal_email_in",
            "placeholder": "Enter your email",
        }
    )
    password = forms.CharField(label="")
    password.widget.attrs.update(
        {
            "type": "password",
            "class": "form-control",
            "id": "id_modal_password_in",
            "placeholder": "Enter your password",
        }
    )
