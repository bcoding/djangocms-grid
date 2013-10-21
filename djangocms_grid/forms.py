from django import forms
from djangocms_grid.models import Grid, GRID_CONFIG, DJANGOCMS_GRID_CHOICES
from django.utils.translation import ugettext_lazy as _
import math

NUM_COLUMNS = [
    (i, '%s' % i) for i in range(0, GRID_CONFIG['COLUMNS'])
]

TOTAL_COLUMNS = GRID_CONFIG['COLUMNS']

TEMPLATE_CHOICES_DATA = [
    (None, 'keine'),
    ([math.floor(TOTAL_COLUMNS/3)*2, math.floor(TOTAL_COLUMNS/3)], '3/1'),
    ([math.floor(TOTAL_COLUMNS/3), math.floor(TOTAL_COLUMNS/3)*2], '1/3'),
    ([math.floor(TOTAL_COLUMNS/2), math.floor(TOTAL_COLUMNS/2)], '2/2'),
    ([math.floor(TOTAL_COLUMNS/3), math.floor(TOTAL_COLUMNS/3), math.floor(TOTAL_COLUMNS/3)], '1/1/1'),
]

TEMPLATE_CHOICES = [(i, TEMPLATE_CHOICES_DATA[i][1]) for i in range(0, len(TEMPLATE_CHOICES_DATA))]

class GridPluginForm(forms.ModelForm):
    create = forms.ChoiceField(choices=NUM_COLUMNS, label=_('Create Columns'), help_text=_('Create this number of columns inside'))
    create_template = forms.ChoiceField(choices=TEMPLATE_CHOICES, label=_('Template'))
    create_size = forms.ChoiceField(choices=DJANGOCMS_GRID_CHOICES, label=_('Column size'), help_text=('Width of created columns. You can still change the width of the column afterwards.'))

    class Meta:
        model = Grid
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
