from django.forms import ModelForm
from bboard.models import Bb


class BbForm(ModeForm):
    class Meta:
        model = Bbfields = ('title', 'content', 'price', 'rubric')