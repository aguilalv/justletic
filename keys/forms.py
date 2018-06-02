from django import forms


class HeroForm(forms.Form):
    EMAIL_FIELD_ERROR = "Please enter a valid email"

    def __init__(self,*args,**kwargs):
        super(HeroForm,self).__init__(*args,**kwargs)
        self.fields['email'].error_messages['required'] = self.EMAIL_FIELD_ERROR
        self.fields['email'].error_messages['invalid'] = self.EMAIL_FIELD_ERROR


    email = forms.EmailField(label='')
#        label='',
#        error_messages={'required': EMAIL_FIELD_ERROR})
    email.widget.attrs.update({
        'class': 'form-control',
        'id':'id_email_in',
        'placeholder':'Enter your email'
    })

