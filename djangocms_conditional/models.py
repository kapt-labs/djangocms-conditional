# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


MODE_IN_GROUP = 'in_group'
MODE_NOT_IN_GROUP = 'not_in_group'
MODE_NOT_IN_GROUP_PLUS_ANON = 'not_in_group_plus_anon'
MODE_ANONYMOUS = 'anonymous'


class ConditionalPluginModel(CMSPlugin):

    permitted_group = models.ForeignKey(Group, null=False, blank=False, on_delete=models.CASCADE)
    mode = models.CharField(max_length=40,
                            default='in_group',
                            help_text=_("Conditional access type"),
                            choices=((MODE_IN_GROUP, _('Users in group')),
                                     (MODE_NOT_IN_GROUP, _('Users not in group')),
                                     (MODE_NOT_IN_GROUP_PLUS_ANON, _('Anonymous users and users not in group')),
                                     (MODE_ANONYMOUS, _('Anonymous users')),
                                     ))

    def __str__(self):
        return _('Conditional access %s group="%s"') % (
            self.mode,
            self.permitted_group.name,
        )
