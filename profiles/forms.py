from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class RegisterForm(UserCreationForm):
    email = forms.EmailField()   

    # Uni-form
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('username', css_class='input-xlarge'),
        Field('email', css_class='input-xlarge'),
        'password1',
        'password2',
        # Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
        # AppendedText('appended_text', '.00'),
        # PrependedText('prepended_text', '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
        PrependedText('prepended_text_two', '@'),
        'multicolon_select',
        FormActions(
            Submit('register', 'register', css_class="btn-primary"),
            # Submit('cancel', 'Cancel'),
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]