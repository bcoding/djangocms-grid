from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.models import CMSPlugin
import math
from django.utils.translation import ugettext_lazy as _

GRID_CONFIG = {'COLUMNS': 24, 'TOTAL_WIDTH': 960, 'GUTTER': 20}
GRID_CONFIG.update(getattr(settings, 'DJANGOCMS_GRID_CONFIG', {}))

DJANGOCMS_GRID_CHOICES = [(None, _('automatic'))] + [
    ('%s' % i, 'grid-%s' % i) for i in range(1, GRID_CONFIG['COLUMNS']+1)
]


class Grid(CMSPlugin):
    inner = models.BooleanField(_('inner'), default=True, help_text=_('Defines whether the plugin is already inside a grid container or another Multi-column plugin.'))
    custom_classes = models.CharField(_('custom classes'), max_length=200, blank=True)

    def __unicode__(self):
        return _(u"%s columns") % self.cmsplugin_set.all().count()


class GridColumn(CMSPlugin):
    size = models.CharField(_('size'), choices=DJANGOCMS_GRID_CHOICES, max_length=50, blank=True, null=True)
    custom_classes = models.CharField(_('custom classes'), max_length=200, blank=True)

    @property
    def actual_size(self):
        """
        The actual size is either the size value set in the model or a value calculated from the number
        of columns and the grid size
        """
        if self.size is not None:
            return self.size
        try:
            grid = Grid.objects.get(cmsplugin_ptr=self.parent)
        except Grid.DoesNotExist:
            return 1
        print "parent: %s" % grid
        
        filled_columns = 0
        auto_columns = 0
        for column in grid.cmsplugin_set.all():
            size = column.gridcolumn.size
            if size is not None:
                filled_columns += int(size)
            else:
                auto_columns += 1
        
        free_columns = GRID_CONFIG['COLUMNS'] - filled_columns
        calculated_size = math.floor(free_columns/auto_columns)
        return int(calculated_size)

    def __unicode__(self):
        return u"%s" % (self.get_size_display() if self.size is not None else _('automatic'))
