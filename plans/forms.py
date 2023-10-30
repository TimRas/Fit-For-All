from django import forms
from .models import Category, Challenge


class ChallengeForm(forms.ModelForm):
    """ A form for creating or updating challenge information. """

    class Meta:
        model = Challenge
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()

        choices = [(c.id, c.title) for c in categories]

        self.fields['category'].choices = choices

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
