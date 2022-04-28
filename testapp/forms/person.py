from django.core.exceptions import ValidationError
from django.forms import fields, forms, models, widgets

from formset.widgets import Selectize, SelectizeMultiple, UploadedFileInput, DualSortableSelector, DualSelector

from testapp.models import PersonModel


class SimplePersonForm(forms.Form):
    """
    This is a simple form used to show how to withhold various feedback messages nearby the
    offending fields. This is done by adding the attribute ``withhold-feedback="..."`` with one
    or a combination of those values: ``messages``, ``errors``, ``warnings`` and/or ``success``.
    """
    last_name = fields.CharField(
        label="Last name",
        min_length=2,
        max_length=50,
        help_text="Please enter at least two characters",
    )

    first_name = fields.RegexField(
        r'^[A-Z][a-z -]*$',
        label="First name",
        error_messages={'invalid': "A first name must start in upper case."},
        help_text="Must start in upper case followed by one or more lowercase characters.",
        max_length=50,
    )


class PersonForm(SimplePersonForm):
    def clean(self):
        cd = super().clean()
        if cd.get('first_name', '').lower().startswith("john") and cd.get('last_name', '').lower().startswith("doe"):
            raise ValidationError(f"{cd['first_name']} {cd['last_name']} is persona non grata here!")
        return cd


sample_person_data = {
    'first_name': "John",
    'last_name': "Doe",
}


class ModelPersonForm(models.ModelForm):
    """
    This form is created by Django's helper functions that creates a Form class out of a Django model.

    The only caveat is that some of the default widgets must or shall be overridden by counterparts from the
    **django-formset** library. For model fields of type ``django.db.models.FileField`` and
    ``django.db.models.ImageField`` the widget **must** be replaced by ``formset.widgets.UploadedFileInput``.

    Input fields for selecting one or more options can be replaced by widgets of type ``formset.widgets.Selectize``,
    ``formset.widgets.SelectizeMutiple`` or ``formset.widgets.DualSelector``.

    To adopt the widgets, specify a dictionary inside the form's ``Meta`` class, for instance

    .. code-block:: python

        class ModelPersonForm(models.ModelForm):
            class Meta:
                model = PersonModel
                fields = '__all__'
                widgets = {
                    'avatar': UploadedFileInput,
                    'gender': widgets.RadioSelect,
                    'opinion': Selectize(search_lookup='label__icontains'),
                    'opinions': SelectizeMultiple(search_lookup='label__icontains', max_items=15),
                }
    """

    class Meta:
        model = PersonModel
        # fields = '__all__'
        fields = ['weighted_opinions']
        widgets = {
            'avatar': UploadedFileInput,
            'gender': widgets.RadioSelect,
            'opinion': Selectize(search_lookup='label__icontains'),
            'opinions': SelectizeMultiple(search_lookup='label__icontains', max_items=15),
            'weighted_opinions': DualSortableSelector(search_lookup='label__icontains'),
        }
