from django.forms import ModelForm
from django.contrib.auth import forms as authforms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from registration.forms import RegistrationForm
from wseeruploader.apps.fileupload import models

class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'New Project'))
    class Meta:
        model = models.Project
        fields = ['name']
        exclude = ('user')

class UploadedFileForm(ModelForm):
    #def clean_file(self):
        #file = self.cleaned_data.get("file", False)
    #    logger.debug("***File***")
        #logger.debug(file)
            
    class Meta:
        model = models.UploadedFile
        exclude = ('project',)

class BootstrapRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Register'))

class BootstrapAuthenticationForm(authforms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Log In'))

class BootstrapPasswordChangeForm(authforms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Change'))

class BootstrapPasswordResetForm(authforms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Reset'))

class BootstrapSetPasswordForm(authforms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('save', 'Submit'))