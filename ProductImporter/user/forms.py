from django import forms
from ProductImporter.user.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserCreationForm(forms.ModelForm):

    """
    A form for creating new users.
    Includes all the required fields, plus a repeated password.
    """

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'mandatory_mobile':
            _('Mobile Number is mandatory for creating a Staff User')
    }
    email = forms.EmailField(label=_("Email Address"), max_length=254)

    class Meta:
        model = User
        fields = '__all__'
        help_texts = {
            'phone_number': _(
                "Customer's primary mobile number e.g. %s{10 digit mobile number}" % settings.ACTIVE_COUNTRY_CODE)
        }

    def clean_email(self):
        """
        Clean form email.
        :return str email: cleaned email
        :raise forms.ValidationError: Email is duplicated
        """
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        if self.instance:
            user = User.objects.filter(email__iexact=email).exclude(id=self.instance.id)
        else:
            user = User.objects.filter(email__iexact=email)

        if user.exists():
            raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )
        return email

    def save(self, commit=True):
        """
        Save user.
        Save the provided password in hashed format.
        :return users.models.User: user
        """
        user = super(UserCreationForm, self).save(commit=False)
        if not self.instance:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user