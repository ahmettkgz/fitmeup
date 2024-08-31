from django.forms.widgets import Textarea


class CustomTextarea(Textarea):
    default_attrs = {"cols": "87", "rows": "10"}

    def __init__(self, attrs=None):
        if attrs:
            self.default_attrs.update(attrs)
        super().__init__(self.default_attrs)
