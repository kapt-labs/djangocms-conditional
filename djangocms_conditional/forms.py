from django import forms
from django.utils.translation import gettext as _
from .models import MODE_IN_GROUP, MODE_NOT_IN_GROUP, MODE_NOT_IN_GROUP_PLUS_ANON


class ConditionalPluginForm(forms.ModelForm):
    fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        permitted_group = cleaned_data.get("permitted_group")
        mode = cleaned_data.get("mode")
        modes_that_require_group = [
            MODE_IN_GROUP,
            MODE_NOT_IN_GROUP,
            MODE_NOT_IN_GROUP_PLUS_ANON
        ]

        if mode in modes_that_require_group and permitted_group is None:
            self.add_error("permitted_group", _("You must choose a group when using this mode."))
